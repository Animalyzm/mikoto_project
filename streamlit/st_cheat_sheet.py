# https://docs.streamlit.io/
# https://docs.streamlit.io/develop/quick-reference/cheat-sheet

import numpy as np  # v2.2.5
import pandas as pd  # v2.2.3
import streamlit as st  # v1.45.1
from streamlit.components.v1 import html  # JavaScript 用

# テキスト関連表示
st.write('write')
st.text('text')
st.markdown('- markdown')
st.json({'json': 123})
st.latex(r""" LaTex: y = x^2 + \frac{1}{x} """)
st.badge('badge')

st.markdown('---')

# HTML などを使う
st.html('<h1 style="color: lime;">html</h1>')
html("<script>alert('JS!');</script>")

st.markdown('---')

# 画像表示
# st.image('../django/tutorial/app/static/fuji.jpg', width=300)
# 音声
# st.audio()
# 動画
# st.video()

st.markdown('---')

# データ･チャート表示
df = pd.DataFrame({
    'x': np.random.randn(10),
    'y': np.random.randn(10)
})
st.dataframe(df.T, height=120, hide_index=False)
left_col, right_col = st.columns([2, 2])
left_col.line_chart(df, height=250)
left_col.bar_chart(df, height=250)
right_col.area_chart(df, height=250)
right_col.scatter_chart(df, height=250)

# 地図表示
df = pd.DataFrame({
    'latitude': np.random.randn(10)+35,
    'longitude': np.random.randn(10)+135
})
st.dataframe(df.T.round(2), height=120, hide_index=False)
st.map(df)

st.markdown('---')

# サイドバー、画面分割、タブ
# サイドバー
st.sidebar.markdown('# sidebar')
# 画面分割
left_col, right_col = st.columns([2, 1])
left_col.markdown('### left_col')
right_col.markdown('### right_col')
st.markdown('---')
# タブ
main_tab, sub_tab = st.tabs(['main_tab', 'sub_tab'])
main_tab.markdown('### main_tab')
sub_tab.markdown('### sub_tab')

st.markdown('---')

# 入力ウィジェット
# https://docs.streamlit.io/develop/api-reference/widgets
# ボタン
if st.button('クリック'):
    st.markdown('クリックされたよ♪')
# チェック･ボックス
check = st.checkbox('チェック')
st.markdown(check)
# セレクト･ボックス
select = st.selectbox('セレクト', ['Dog', 'Cat', 'Lion'])
st.markdown(select)
# 日付入力
date = st.date_input('日付')
st.markdown(date)
# テキスト入力
input_text = st.text_input('テキスト')
st.markdown(input_text)

# streamlit run st_cheat_sheet.py 8501
