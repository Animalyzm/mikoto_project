import binascii
import datetime as dt
import hashlib
import json
from typing import Tuple

from ecdsa import SECP256k1, SigningKey, VerifyingKey
import requests


POW_ZEROS = 3


def verify_block_chain(block_chain: list) -> bool:
    # 1. 前ブロックのハッシュ値の確認
    if make_hash_str(block_chain[-2]) != block_chain[-1]['hash']:
        return False
    # 2. トランザクション検証
    new_block_transactions = block_chain[-1]['transactions']
    for transaction in new_block_transactions:
        if transaction['sender'] != 'mikoto_project':
            if not verify_data(transaction, transaction['sender']):
                return False
    # 3. 検証済みとの重複確認(今回は空)
    verified_transactions = []
    for block in block_chain[:-1]:
        verified_transactions += block['transactions']
    for transaction in new_block_transactions:
        if transaction in verified_transactions:
            return False
    # 4. 新ブロック内での重複確認（signature で確認）
    signature_list = []
    for transaction in new_block_transactions:
        if transaction['sender'] != 'mikoto_project':
            signature_list.append(transaction['signature'])
    if len(signature_list) != len(set(signature_list)):
        return False
    # 5. proof_of_work 確認
    copy_new_block = block_chain[-1].copy()
    copy_new_block.pop('time')
    if not make_hash_str(copy_new_block).startswith('0'*POW_ZEROS):
        return False
    return True


def mining(transaction_pool: list, block_chain: list, miner_public_key_str: str, mik: int) -> dict:
    verified_transactions = []
    for block in block_chain:
        verified_transactions += block['transactions']  # 検証済
    for transaction in transaction_pool:
        if transaction in verified_transactions:  # 重複チェック
            transaction_pool.remove(transaction)
            continue
        if transaction['sender'] != 'mikoto_project':
            if not verify_data(transaction, transaction['sender']):
                transaction_pool.remove(transaction)
    mikoto_transaction = make_mikoto_transaction(miner_public_key_str, mik)
    transaction_pool.append(mikoto_transaction)
    previous_block_hash_str = make_hash_str(block_chain[-1])
    new_block = {
        'transactions': transaction_pool,
        'hash': previous_block_hash_str,
        'nonce': 0
    }
    new_block = proof_of_work(new_block)  # nonce, PoW
    new_block['time'] = dt.datetime.now().isoformat()
    keys = ['time', 'transactions', 'hash', 'nonce']
    sorted_new_block = {key: new_block[key] for key in keys}
    return sorted_new_block


def proof_of_work(block: dict, zeros=POW_ZEROS) -> dict:
    while not make_hash_str(block).startswith('0'*zeros):
        block['nonce'] += 1
    return block


def make_hash_str(data: dict) -> str:
    return hashlib.sha256(json.dumps(data).encode('utf-8')).hexdigest()


def get_data(url: str) -> requests.Response:
    return requests.get(url)


def make_thanks_transaction(
        sender_secret_key_str: str, sender_public_key_str: str,
        receiver_public_key_str: str, mik: int) -> dict:
    thanks_transaction = {
        'time': dt.datetime.now().isoformat(),
        'sender': sender_public_key_str,
        'receiver': receiver_public_key_str,
        'MIK': mik,
    }
    signature = make_signature_str(
        thanks_transaction, sender_secret_key_str)
    thanks_transaction['signature'] = signature
    return thanks_transaction


def make_mikoto_transaction(receiver_public_key_str: str, mik: int) -> dict:
    mikoto_transaction = {
        'time': dt.datetime.now().isoformat(),
        'sender': 'mikoto_project',
        'receiver': receiver_public_key_str,
        'MIK': mik,
        'signature': 'mikoto_project',
    }
    return mikoto_transaction


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
