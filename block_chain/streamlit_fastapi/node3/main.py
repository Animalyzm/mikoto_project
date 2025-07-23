from fastapi import FastAPI
from pydantic import BaseModel

import mikoto as mik


class Test(BaseModel):
    test1: str
    test2: int


class KeyData(BaseModel):
    name: str
    url: str
    public_key_str: str
    signature: str


app = FastAPI()


@app.get('/')
async def index():
    return "Welcome to Mikoto Project!"


@app.post('/test')
async def post_test(data: Test) -> dict:
    return {"message": "test pass"}


@app.post('/key_data')
async def post_key_data(key_data: KeyData):
    key_data = dict(key_data)
    print(key_data)
    if not mik.verify_data(key_data, key_data['public_key_str']):
        return {"message": "key_data invalid"}
    key_data.pop('signature')
    key_data_list = mik.load_json('json/key_data_list.json')
    key_data_list.append(key_data)
    mik.save_json(key_data_list, 'json/key_data_list.json')
    return {"message": "key_data received"}


# uvicorn main:app --reload --port 8012
