import binascii
import datetime as dt
import json
from typing import Tuple

from ecdsa import SECP256k1, SigningKey, VerifyingKey
import requests


def public_key_str_search(public_key_str: str) -> bool:
    key_data_list = load_json('json/key_data_list.json')
    public_key_str_list = [key_data['public_key_str'] for key_data in key_data_list]
    return public_key_str in public_key_str_list


def make_login_data(path: str) -> Tuple[dict, str]:
    my_data = load_json(path)
    login_data = {
        'time': dt.datetime.now().isoformat(),
        'public_key_str': my_data['public_key_str']
    }
    signature = make_signature_str(login_data, my_data['secret_key_str'])
    login_data['signature'] = signature
    return login_data, my_data['url']


def get_url_list(base_path='json/') -> list:
    key_data_list = load_json(base_path + 'key_data_list.json')
    url_list = [key_data['url'] for key_data in key_data_list]
    return url_list


def make_first_node(save_dir: str = 'json/') -> None:
    """
    実行コマンド
    python -c "import mikoto; mikoto.make_first_node()"
    """
    name = input('name: ')
    url = input('url: ')
    key_data = make_key_data(name, url)
    save_json(key_data, save_dir+'.my_data.json')
    block_chain = [
        {
            'time': dt.datetime.now().isoformat(),
            'transactions': [],
            'hash': 'mikoto_block_chain',
            'nonce': 0
        }
    ]
    save_json(block_chain, save_dir+'block_chain.json')
    key_data_list = []
    key_data.pop('secret_key_str')
    key_data_list.append(key_data)
    save_json(key_data_list, save_dir+'key_data_list.json')
    transaction_pool = []
    save_json(transaction_pool, save_dir+'transaction_pool.json')
    print("made first_node")
    return None


def verify_data(data: dict, public_key_str:str) -> bool:
    """ need key: signature """
    try:
        public_key = str_to_public_key(public_key_str)
        signature = binascii.unhexlify(data['signature'])
        copy_data = data.copy()
        copy_data.pop('signature')
        public_key.verify(signature, json.dumps(copy_data).encode('utf-8'))
        return True
    except:
        return False


def post_data(url: str, data: dict)-> requests.Response:
    return requests.post(url, json.dumps(data))


def make_signature_str(data: dict, secret_key_str: str) -> str:
    secret_key = str_to_secret_key(secret_key_str)
    return secret_key.sign(json.dumps(data).encode('utf-8')).hex()


def load_json(path: str) -> list | dict:
    with open(path, mode='r') as f:
        data = json.load(f)
    return data


def save_json(data: list | dict, path: str) -> None:
    with open(path, mode='w') as f:
        json.dump(data, f)
    return None


def make_key_data(name: str, url: str) -> dict:
    secret_key = make_secret_key()
    secret_key_str = key_to_str(secret_key)
    public_key = make_public_key(secret_key)
    public_key_str = key_to_str(public_key)
    key_data = {
        'name': name,
        'url': url,
        'secret_key_str': secret_key_str,
        'public_key_str': public_key_str
    }
    return key_data


def str_to_public_key(public_key_str: str) -> VerifyingKey:
    return VerifyingKey.from_string(binascii.unhexlify(public_key_str), curve=SECP256k1)


def str_to_secret_key(secret_key_str: str) -> SigningKey:
    return SigningKey.from_string(binascii.unhexlify(secret_key_str), curve=SECP256k1)


def key_to_str(key: SigningKey | VerifyingKey) -> str:
    return key.to_string().hex()


def make_public_key(secret_key: SigningKey) -> VerifyingKey:
    return secret_key.verifying_key


def make_secret_key() -> SigningKey:
    return SigningKey.generate(curve=SECP256k1)
