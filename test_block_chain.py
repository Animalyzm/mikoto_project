import binascii
import copy
import datetime as dt
import json

from ecdsa import SECP256k1, SigningKey, VerifyingKey

import block_chain as bc


# テスト用のデータ作成
name_list = ['Dog', 'Cat', 'Lion']
user_info_dict = {}
for name in name_list:
    user_info_dict[name] = bc.make_key_data()
transaction_pool = []
transaction_pool.append(
    bc.make_mikoto_trasaction(user_info_dict['Dog']['public_key_str'], 100)
)
transaction_pool.append(
    bc.make_thanks_transaction(
        user_info_dict['Dog']['secret_key_str'],
        user_info_dict['Dog']['public_key_str'],
        user_info_dict['Cat']['public_key_str'],
        10
    )
)
transaction_pool.append(
    bc.make_thanks_transaction(
        user_info_dict['Dog']['secret_key_str'],
        user_info_dict['Dog']['public_key_str'],
        user_info_dict['Lion']['public_key_str'],
        20
    )
)
block_chain = bc.make_first_block_chain()
sorted_new_block = bc.mining(transaction_pool, block_chain, user_info_dict['Dog']['public_key_str'], 100)
block_chain.append(sorted_new_block)


def test_verify_block_chain():
    """ test: True case, False case """
    # テスト用データ：block_chain
    # True case
    assert bc.verify_block_chain(block_chain)
    # False case: fake_hash
    fake_hash_block_chain = copy.deepcopy(block_chain)
    fake_hash_block_chain[-1]['hash'] = ''
    assert bc.verify_block_chain(fake_hash_block_chain) is False
    # False case: fake_transaction
    fake_transaction_block_chain = copy.deepcopy(block_chain)
    fake_signature = fake_transaction_block_chain[-1]['transactions'][-2]['signature']
    fake_transaction_block_chain[-1]['transactions'][-3]['signature'] = fake_signature
    assert bc.verify_block_chain(fake_transaction_block_chain) is False
    # Flase case: dupulicates_transaction
    dupulicates_transaction_bc = copy.deepcopy(block_chain)
    dupulicate_transaction = dupulicates_transaction_bc[-1]['transactions'][-2]
    dupulicates_transaction_bc[-2]['transactions'].append(dupulicate_transaction)
    dupulicates_transaction_bc[-1]['hash'] = bc.make_hash_str(dupulicates_transaction_bc[-2])
    def re_proof_of_work(block):
        """ nonceを計算し直す """
        nonce_dict = {k: v for k, v in block.items() if k != 'time'}
        nonce_dict['nonce'] = 0
        nonce_dict = bc.proof_of_work(nonce_dict)
        block['nonce'] = nonce_dict['nonce']
        return block
    dupulicates_transaction_bc[-1] = re_proof_of_work(dupulicates_transaction_bc[-1])
    assert bc.verify_block_chain(dupulicates_transaction_bc) is False
    # False case: new_block_dupulicates_transaction
    new_block_dupulicates_transaction_bc = copy.deepcopy(block_chain)
    dupulicate_transaction = new_block_dupulicates_transaction_bc[-1]['transactions'][-2]
    new_block_dupulicates_transaction_bc[-1]['transactions'].append(dupulicate_transaction)
    new_block_dupulicates_transaction_bc[-1] = re_proof_of_work(new_block_dupulicates_transaction_bc[-1])
    assert bc.verify_block_chain(new_block_dupulicates_transaction_bc) is False
    # False case: fake_pow
    fake_pow_block_chain = copy.deepcopy(block_chain)
    if fake_pow_block_chain[-1]['nonce'] != 0:
        fake_pow_block_chain[-1]['nonce'] = 0
    else:
        fake_pow_block_chain[-1]['nonce'] = 1
    assert bc.verify_block_chain(fake_pow_block_chain) is False
    

def test_mining():
    """ test: type, keys """
    block_chain = bc.make_first_block_chain()
    # テスト用データ
    miner_public_key_str = user_info_dict['Dog']['public_key_str']
    MIK = 100
    # テスト用データ：transaction_pool
    sorted_new_block = bc.mining(transaction_pool, block_chain, miner_public_key_str, MIK)
    keys = ['time', 'transactions', 'hash', 'nonce']
    assert isinstance(sorted_new_block, dict)
    assert list(sorted_new_block.keys()) == keys
    assert dt.datetime.fromisoformat(sorted_new_block['time'])
    assert isinstance(sorted_new_block['transactions'], list)
    assert isinstance(sorted_new_block['hash'], str)
    assert isinstance(sorted_new_block['nonce'], int)


def test_proof_of_work():
    """ test: type, len, zeros """
    POW_ZEROS = 3
    block = bc.make_first_block_chain()[0]
    block = bc.proof_of_work(block, POW_ZEROS)
    hash_value = bc.make_hash_str(block)
    assert isinstance(hash_value, str)
    assert len(hash_value) == 64
    assert hash_value.startswith('0'*POW_ZEROS)


def test_make_first_block_chain():
    """ test: type, keys, value """
    first_block_chain = bc.make_first_block_chain()
    keys = ['time', 'transactions', 'hash', 'nonce']
    assert isinstance(first_block_chain, list)
    assert isinstance(first_block_chain[0], dict)
    assert list(first_block_chain[0].keys()) == keys
    assert dt.datetime.fromisoformat(first_block_chain[0]['time'])
    assert first_block_chain[0]['transactions'] == []
    assert first_block_chain[0]['hash'] == 'mikoto_project'
    assert first_block_chain[0]['nonce'] == 0


def test_make_hash_str():
    """ test: type, len, change """
    list_data = list(range(5))
    list_hash_str = bc.make_hash_str(list_data)
    assert isinstance(list_hash_str, str)
    assert len(list_hash_str) == 64
    dict_data1 = {'a': 1, 'b': 2}
    dict_data2 = {'a': 1, 'b': 3}
    dict_hash_str1 = bc.make_hash_str(dict_data1)
    dict_hash_str2 = bc.make_hash_str(dict_data2)
    assert isinstance(dict_hash_str1, str)
    assert len(dict_hash_str1) == 64
    assert dict_hash_str1 != dict_hash_str2


def test_verify_transaction():
    """ test: True case, False case"""
    # テスト用データ
    thanks_trasaction = transaction_pool[1]
    assert bc.verify_transaction(thanks_trasaction)
    # receiver と sender を逆にする
    sender = thanks_trasaction['receiver']
    receiver = thanks_trasaction['sender']
    thanks_trasaction['sender'] = sender
    thanks_trasaction['receiver'] = receiver
    assert bc.verify_transaction(thanks_trasaction) is False


def test_make_thanks_transaction():
    """ test: type, keys, conversion, value, verify """
    # テスト用データ
    sender_secret_key_str = user_info_dict['Dog']['secret_key_str']
    sender_public_key_str = user_info_dict['Dog']['public_key_str']
    receiver_public_key_str = user_info_dict['Cat']['public_key_str']
    MIK = 10
    thanks_transaction = bc.make_thanks_transaction(
        sender_secret_key_str, sender_public_key_str, 
        receiver_public_key_str, MIK
    )
    assert isinstance(thanks_transaction, dict)
    assert list(thanks_transaction.keys()) == ['time', 'sender', 'receiver', 'MIK', 'signature']
    # datetime 型に変換
    assert dt.datetime.fromisoformat(thanks_transaction['time'])
    assert thanks_transaction['sender'] == sender_public_key_str
    assert thanks_transaction['receiver'] == receiver_public_key_str
    assert isinstance(thanks_transaction['MIK'], int)
    # verify
    signature = binascii.unhexlify(thanks_transaction['signature'])
    thanks_transaction.pop('signature')
    sender_public_key = VerifyingKey.from_string(binascii.unhexlify(sender_public_key_str), curve=SECP256k1)
    assert sender_public_key.verify(signature, json.dumps(thanks_transaction).encode('utf-8'))


def test_make_mikoto_trasaction():
    """ test: type, keys, conversion, value """
    # テスト用データ
    receiver_public_key_str = user_info_dict['Dog']['public_key_str']
    MIK = 100
    mikoto_transaction = bc.make_mikoto_trasaction(receiver_public_key_str, MIK)
    assert isinstance(mikoto_transaction, dict)
    assert list(mikoto_transaction.keys()) == ['time', 'sender', 'receiver', 'MIK', 'signature']
    # datetime 型に変換
    assert dt.datetime.fromisoformat(mikoto_transaction['time'])
    assert mikoto_transaction['sender'] == 'mikoto_project'
    assert mikoto_transaction['receiver'] == receiver_public_key_str
    assert isinstance(mikoto_transaction['MIK'], int)
    assert mikoto_transaction['signature'] == 'mikoto_project'


def test_make_key_data():
    """ test: type, str_to_key """
    key_data = bc.make_key_data()
    assert isinstance(key_data, dict)
    assert SigningKey.from_string(
        binascii.unhexlify(key_data['secret_key_str']), curve=SECP256k1
    )
    assert VerifyingKey.from_string(
        binascii.unhexlify(key_data['public_key_str']), curve=SECP256k1
    )
