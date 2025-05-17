from fastapi.testclient import TestClient
from streamlit.testing.v1 import AppTest

from main import app


""" main.py 用テスト """
client = TestClient(app)


def test_main_read_root():
    """ test: status, json """
    response = client.get("/")  # URL を省略できます
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_main_read_root_error():
    """ test: status """
    response = client.get("/1")  # 存在しない URL
    assert response.status_code == 404


def test_main_post_test():
    """ test: status, json """
    response = client.post('/test', json={"data": "test"})
    assert response.status_code == 200
    assert response.json() == {"message": "data received"}


def test_main_post_test_error():
    """ test: status """
    response = client.post('/test', json="data")  # 違うデータ構造
    assert response.status_code == 422
    response = client.post('/test1', json={"data": "test"})
    assert response.status_code == 404



""" app.py 用テスト """
def test_app_json():
    """ test: value """
    at = AppTest.from_file("app.py").run()
    assert at.json[0].value == '{"message": "Hello world!"}'


def test_app_button():
    """ test: click """
    at = AppTest.from_file("app.py").run()
    assert at.button(key='test').click()


# 実行: pytest test_app_main.py
