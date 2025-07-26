from fastapi import FastAPI
from pydantic import BaseModel

import log
import mikoto as mik


logger = log.get_logger('main')
log.basic_config('debug', 'block_chain.log')


class Test(BaseModel):
    test1: str
    test2: int


class KeyData(BaseModel):
    name: str
    url: str
    public_key_str: str
    signature: str


class LoginData(BaseModel):
    time: str
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
        log.log_error(logger, 'key_data invalid')
        return {"message": "key_data invalid"}
    key_data.pop('signature')
    key_data_list = mik.load_json('json/key_data_list.json')
    key_data_list.append(key_data)
    mik.save_json(key_data_list, 'json/key_data_list.json')
    log.log_debug(logger, 'key_data received')
    return {"message": "key_data received"}


@app.post('/login_data')
async def post_login_data(login_data: LoginData):
    login_data = dict(login_data)
    if mik.public_key_str_search(login_data['public_key_str']):
        if mik.verify_data(login_data, login_data['public_key_str']):
            log.log_debug(logger, 'login_data valid')
            return {"message": "login_data valid"}
        else:
            log.log_error(logger, 'login_data invalid')
            return  {"message": "login_data invalid"}
    else:
        log.log_error(logger, 'public_key_str invalid')
        return {"message": "public_key_str invalid"}


# uvicorn main:app --reload --port 8012
