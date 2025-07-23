from fastapi.testclient import TestClient
from streamlit.testing.v1 import AppTest

from main import app


""" app.py(Streamlit) """
def test_app():
    at = AppTest.from_file("app.py").run()
    assert at.markdown[0].value == "### みことプロジェクト"


""" main.py(FastAPI) """
client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Welcome to Mikoto Project!"


def test_post_test():
    """ test: status, message """
    test_data = {'test1': 'animal', 'test2': 100}
    response = client.post(
        "/test",
        json=test_data,
    )
    assert response.status_code == 200
    assert response.json() == {"message": "test pass"}
