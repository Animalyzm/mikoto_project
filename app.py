import json

import requests

import streamlit as st


st.json({"message": "Hello world!"})

if st.button('テスト', key='test'):
    data = {"data": "test"}
    res = requests.post('http://127.0.0.1:8010/test', json.dumps(data))
    st.json(res.json())


# サーバー起動: streamlit run app.py --server.port 8501
