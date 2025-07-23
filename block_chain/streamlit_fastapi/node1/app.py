import os

import streamlit as st

import mikoto as mik


st.markdown("### みことプロジェクト")

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
                st.json(res.json())
            except:
                st.json({"message": f"{url}: error"})
        # 認証率合格なら保存
        if res_200_count / len(url_list) > 0.9:
            mik.save_json(key_data, "json/.my_data.json")
        else:
            st.json({"message": "key_data invalid"})

else:
    st.markdown("鍵作成済の場合の表示")


# streamlit run app.py --server.port 8501
