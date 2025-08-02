import os

import streamlit as st
from pandas.core.internals.blocks import new_block

import log
import mikoto as mik


logger = log.get_logger('app')
log.basic_config('debug', 'block_chain.log')


st.markdown("### みことプロジェクト")


def change_state(ss):
    if ss.state is True:
        ss.state = False
        ss.label = 'ログイン'
        log.log_debug(logger, 'logout')
    else:
        login_data, url = mik.make_login_data('json/.my_data.json')
        try:
            response = mik.post_data(url+'/login_data', login_data)
            if response.json() == {"message": "login_data valid"}:
                ss.state = True
                ss.label = 'ログアウト'
                log.log_debug(logger, 'login')
            else:
                ss.label = 'ログインできませんでした'
                log.log_error(logger, 'login failed')
        except:
            ss.label = 'ログインできませんでした'
            log.log_error(logger, 'login failed')

if not os.path.exists('json/.my_data.json'):
    name = st.text_input('ニックネームを入力してください')
    add_url = st.text_input('URL を入力してください')

    if st.button('鍵を作成する', key='make_key'):
        key_data = mik.make_key_data(name, add_url)
        secret_key_str = key_data['secret_key_str']
        send_data = key_data.copy()
        send_data.pop('secret_key_str')
        signature = mik.make_signature_str(send_data, secret_key_str)
        key_data["signature"] = signature

        url_list = mik.get_url_list()
        url_list.append(add_url)
        res_200_count = 0
        for url in url_list:
            try:
                res = mik.post_data(url+'/key_data', key_data)
                if res.status_code == 200:
                    res_200_count += 1
                st.json({"status_code": res.status_code})
                log.log_debug(logger, f'{res}: {res.json()}')
            except:
                st.json({"message": f"{url}: error"})
                log.log_error(logger, f"{url}: error")
        # 認証率合格なら保存
        if res_200_count / len(url_list) > 0.9:
            mik.save_json(key_data, "json/.my_data.json")
            log.log_debug(logger, 'key_data saved')
        else:
            st.json({"message": "key_data invalid"})
            log.log_error(logger, 'key_data invalid')

else:
    st.markdown("鍵作成済の場合の表示")
    # 初期化
    ss = st.session_state
    if 'state' not in ss:
        ss.state = False
    if 'label' not in ss:
        ss.label = 'ログイン'

    st.button(ss.label, key='login', on_click=change_state, args=(ss,))

    if ss.state is True:
        st.markdown('ログイン中')
        menu = ['発行または送信', 'マイニング']
        choice = st.selectbox(label='メニュー', options=menu)
        key_data_list = mik.load_json('json/key_data_list.json')
        my_data = mik.load_json('json/.my_data.json')
        url_list = mik.get_url_list()

        if choice == '発行または送信':
            sender_name = st.selectbox('送り手（mikoto_projectは発行）', [my_data['name'], 'mikoto_project'])

            receiver_name = st.text_input('受け取り手')
            receiver_data = None
            if receiver_name:
                if (sender_name != 'mikoto_project' and
                    receiver_name == my_data['name']):
                    st.markdown('自分には送信できません')
                else:
                    for key_data in key_data_list:
                        if key_data['name'] == receiver_name:
                            receiver_data = key_data
                            st.write(receiver_data)
                    if not receiver_data:
                        st.markdown('登録されていないニックネームです')

            mik_value = st.number_input('MIKの量', min_value=0, step=1)

            if receiver_data and mik_value:
                if st.button('実行する'):
                    if sender_name == 'mikoto_project':
                        transaction = mik.make_mikoto_transaction(
                            receiver_data['public_key_str'],
                            mik_value
                        )
                        st.json(transaction)
                    else:
                        transaction = mik.make_thanks_transaction(
                            my_data['secret_key_str'],
                            my_data['public_key_str'],
                            receiver_data['public_key_str'],
                            mik_value
                        )
                        st.json(transaction)

                    for url in url_list:
                        try:
                            res = mik.post_data(url+'/transaction', transaction)
                            st.json(res.json())
                            log.log_debug(logger, f'{res}: {res.json()}')
                        except:
                            st.json({"message": f"{url}: error"})
                            log.log_error(logger, f"{url}: error")

        if choice == 'マイニング':
            if st.button('マイニングを実行'):
                block_chain = mik.load_json('json/block_chain.json')
                transaction_pool = mik.load_json('json/transaction_pool.json')
                new_block = mik.mining(
                    transaction_pool,
                    block_chain,
                    my_data['public_key_str'],
                    100)
                block_chain.append(new_block)

                for url in url_list:
                    try:
                        res = mik.post_data(url + '/block_chain', block_chain)
                        st.json(res.json())
                        log.log_debug(logger, f'{res}: {res.json()}')
                    except:
                        st.json({"message": f"{url}: error"})
                        log.log_error(logger, f"{url}: error")


    else:
        st.markdown('ログアウト状態')


# streamlit run app.py --server.port 8502
