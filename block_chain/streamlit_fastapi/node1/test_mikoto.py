import binascii
import datetime as dt
import json
import os
import re

from ecdsa import SigningKey, SECP256k1, VerifyingKey
import pytest

import mikoto as mik


online = False
""" True: uvicorn main:app --reload --port 8010 """

""" 共通利用のデータなど """
co_secret_key = SigningKey.generate(curve=SECP256k1)
co_public_key = co_secret_key.verifying_key
co_secret_key_str = co_secret_key.to_string().hex()
co_public_key_str = co_public_key.to_string().hex()
co2_secret_key = SigningKey.generate(curve=SECP256k1)
co2_public_key = co2_secret_key.verifying_key
co2_public_key_str = co2_public_key.to_string().hex()
co_name_list = ['Dog', 'Cat', 'Lion']
co_base_url = 'http://127.0.0.1'
co_port_list = [':8010', ':8011', ':8012']


def test_make_thanks_transaction():
    """ test: type, keys, conversion, value, unhexlify """
    thanks_transaction = mik.make_thanks_transaction(
        co_secret_key_str, co_public_key_str,
        co2_public_key_str, 100
    )
    assert isinstance(thanks_transaction, dict)
    keys = list(thanks_transaction.keys())
    assert keys == ['time', 'sender', 'receiver', 'MIK', 'signature']
    assert dt.datetime.fromisoformat(thanks_transaction['time'])
    assert thanks_transaction['sender'] == co_public_key_str
    assert thanks_transaction['receiver'] == co2_public_key_str
    assert isinstance(thanks_transaction['MIK'], int)
    assert isinstance(thanks_transaction['signature'], str)
    assert binascii.unhexlify(thanks_transaction['signature'])


def test_make_mikoto_trasaction():
    """ test: type, keys, value """
    mikoto_transaction = mik.make_mikoto_transaction(
        co_public_key_str, 100
    )
    assert isinstance(mikoto_transaction, dict)
    assert list(mikoto_transaction.keys()) == ['time', 'sender', 'receiver', 'MIK', 'signature']
    assert dt.datetime.fromisoformat(mikoto_transaction['time'])
    assert mikoto_transaction['sender'] == 'mikoto_project'
    assert mikoto_transaction['receiver'] == co_public_key_str
    assert isinstance(mikoto_transaction['MIK'], int)
    assert mikoto_transaction['signature'] == 'mikoto_project'


def test_public_key_str_search():
    """ test: true case, false case """
    my_data = mik.load_json('json/.my_data.json')
    assert mik.public_key_str_search(my_data['public_key_str'])
    assert not mik.public_key_str_search(co_public_key_str)


def test_make_login_data():
    """ test: type, keys """
    login_data, url = mik.make_login_data(('json/.my_data.json'))
    assert isinstance(login_data, dict)
    assert isinstance(url, str)
    key_list = ['time', 'public_key_str', 'signature']
    assert list(login_data.keys()) == key_list


def test_get_url_list():
    """ test: type, url """
    url_list = mik.get_url_list(base_path=r'json/')
    assert isinstance(url_list, list)
    for url in url_list:
        assert re.match('https?://.+', url)


def test_make_first_node():
    """ かなりややこしくなるため省略 """
    pass


def test_verify_data():
    """ test: true case, false case """
    data = {'name': co_name_list[0]}
    signature = co_secret_key.sign(json.dumps(data).encode('utf-8')).hex()
    data['signature'] = signature
    assert mik.verify_data(data, co_public_key_str)
    data['name'] = co_name_list[1]  # name を改ざん
    assert not mik.verify_data(data, co_public_key_str)


@pytest.mark.skipif(online==False, reason="not online")
def test_post_data():
    test_data = {'test1': 'animal', 'test2': 100}
    response = mik.post_data(co_base_url+co_port_list[0]+'/test', test_data)
    assert response.status_code == 200
    assert response.json() == {"message": "test pass"}


def test_make_signature_str():
    """ test: type, len, unhexlify """
    data = {'public_key': co_public_key_str}
    signature_str = mik.make_signature_str(data, co_secret_key_str)
    assert isinstance(signature_str, str)
    assert len(signature_str) == 128
    assert binascii.unhexlify(signature_str)


def test_save_json():
    """ test: save, (str, list, dict), exist """
    base_path = 'test_data/'
    assert not mik.save_json('str', base_path+'test_str.json')
    assert os.path.exists(base_path+'test_str.json')
    assert not mik.save_json(['list'], base_path+'test_list.json')
    assert os.path.exists(base_path+'test_list.json')
    assert not mik.save_json({'dict': 1}, base_path+'test_dict.json')
    assert os.path.exists(base_path+'test_dict.json')


def test_load_json():
    """ test: load, type(str, list, dict)
    先に test_save_json() を実行する必要あり
    """
    base_path = 'test_data/'
    assert mik.load_json(base_path+'test_str.json')
    str_data = mik.load_json(base_path+'test_str.json')
    assert isinstance(str_data, str)
    assert mik.load_json(base_path+'test_list.json')
    list_data = mik.load_json(base_path+'test_list.json')
    assert isinstance(list_data, list)
    assert mik.load_json(base_path+'test_dict.json')
    dict_data = mik.load_json(base_path+'test_dict.json')
    assert isinstance(dict_data, dict)


def test_make_key_data():
    """ test: type, keys, url, str_to_key """
    key_data = mik.make_key_data(co_name_list[0], co_base_url+co_port_list[0])
    assert isinstance(key_data, dict)
    key_list = ['name', 'url', 'secret_key_str', 'public_key_str']
    assert list(key_data.keys()) == key_list
    assert isinstance(key_data['name'], str)
    assert re.match('https?://.+', key_data['url'])
    assert SigningKey.from_string(binascii.unhexlify(key_data['secret_key_str']), curve=SECP256k1)
    assert VerifyingKey.from_string(binascii.unhexlify(key_data['public_key_str']), curve=SECP256k1)


def test_str_to_public_key():
    """ test: type """
    public_key = mik.str_to_public_key(co_public_key_str)
    assert isinstance(public_key, type(co_public_key))


def test_str_to_secret_key():
    """ test: type """
    secret_key = mik.str_to_secret_key(co_secret_key_str)
    assert isinstance(secret_key, type(co_secret_key))


def test_key_to_str_public_key():
    """ test: type, len """
    public_key_str = mik.key_to_str(co_public_key)
    assert isinstance(public_key_str, str)
    assert len(public_key_str) == 128


def test_key_to_str_secret_key():
    """ test: type, len """
    secret_key_str = mik.key_to_str(co_secret_key)
    assert isinstance(secret_key_str, str)
    assert len(secret_key_str) == 64


def test_make_public_key():
    """ test: type """
    public_key = mik.make_public_key(co_secret_key)
    assert isinstance(public_key, type(co_secret_key.verifying_key))


def test_make_secret_key():
    """ test: type (curve=SECP256k1)"""
    secret_key = mik.make_secret_key()
    secret_key_type = type(co_secret_key)
    assert isinstance(secret_key, secret_key_type)
