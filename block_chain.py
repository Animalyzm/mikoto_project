import binascii
from datetime import datetime
import hashlib
import json
import pprint
from typing import Any

from ecdsa import BadSignatureError, SECP256k1, SigningKey, VerifyingKey


POW_ZEROS = 3 


def verify_block_chain(block_chain: list) -> bool:
    """
    ブロックチェーンを検証する
    1. 前ブロックのハッシュ値確認
    2. proof_of_work 確認
    3. トランザクション検証
    4. 検証済みとの重複確認
    5. 新ブロック内での重複確認
    print: False 時の理由
    """
    # 1. 前ブロックのハッシュ値の確認
    if make_hash_str(block_chain[-2]) != block_chain[-1]['hash']:
        print('hash_str invalid')
        return False
    # 2. proof_of_work 確認
    copy_new_block = block_chain[-1].copy()
    copy_new_block.pop('time')
    if not make_hash_str(copy_new_block).startswith('0'*POW_ZEROS):
        print('proof_of_work invalid')
        return False
    # 3. トランザクション検証
    new_block_transactions = block_chain[-1]['transactions']
    for transaction in new_block_transactions:
        if transaction['sender'] != 'mikoto_project':
            if not verify_transaction(transaction):
                print('transaction invalid')
                print(transaction)
                return False
    # 4. 検証済みとの重複確認(今回は最初のブロックのみなので空)
    verified_transactions = []
    for block in block_chain[:-1]:
        verified_transactions += block['transactions']
    for transaction in new_block_transactions:
        if transaction in verified_transactions:
            print('duplicates invalid')
            return False
    # 5. 新ブロック内での重複確認（signature で確認）
    signature_list = []
    for transaction in new_block_transactions:
        if transaction['sender'] != 'mikoto_project':
            signature_list.append(transaction['signature'])
    if len(signature_list) != len(set(signature_list)):
        print('new_block duplicates invalid')
        return False
    return True


def mining(transaction_pool: list, block_chain: list, miner_public_key_str: str, MIK: int) -> list:
    """
    マイニングする
    1. verified_transactions: 重複チェック
    2. verify_transaction: 検証
    3. make_mikoto_trasaction: MIK 発行（報酬）
    4. proof_of_work: nonce 算出
    """
    verified_transactions = []
    copy_transaction_pool = transaction_pool.copy() # 検証前
    for block in block_chain:
        verified_transactions += block['transactions']
    for transaction in copy_transaction_pool:
        # 1. 重複チェック
        if transaction in verified_transactions:
            copy_transaction_pool.remove(transaction)
            continue
        # 2. 検証
        if transaction['sender'] != 'mikoto_project':
            if not verify_transaction(transaction):
                copy_transaction_pool.remove(transaction)
    # 3. MIK 発行
    mikoto_transaction = make_mikoto_trasaction(miner_public_key_str, MIK)
    copy_transaction_pool.append(mikoto_transaction)
    # 前ブロックのハッシュ値
    previous_block_hash_str = make_hash_str(block_chain[-1])
    new_block = {
        'transactions': copy_transaction_pool,
        'hash': previous_block_hash_str,
        'nonce': 0
    }
    # 4. nonce 算出（proof_of_work, POW）
    new_block = proof_of_work(new_block)
    new_block['time'] = datetime.now().isoformat()
    keys = ['time', 'transactions', 'hash', 'nonce']
    sorted_new_block = {key: new_block[key] for key in keys}
    return sorted_new_block
    

def proof_of_work(block: dict) -> dict:
    """
    ハッシュ値の最初の POW_ZEORS 文字を0にする nonce を算出する
    """
    while not make_hash_str(block).startswith('0'*POW_ZEROS):
        block['nonce'] += 1
    print('proof_of_work hash:', make_hash_str(block))
    return block


def make_first_block_chain() -> list:
    """ 
    最初のブロックチェーンを作る
    return: block list
    block: dict(keys=['time', 'transactions', 'hash', 'nonce'])
    """
    first_block_chain = [
        {
            'time': datetime.now().isoformat(),
            'transactions': [],
            'hash': 'mikoto_project',
            'nonce': 0, 
        }
    ]
    return first_block_chain


def make_hash_str(data: Any) -> str:
    """ return: hash_str(len: 64) """
    hash_str = hashlib.sha256(json.dumps(data).encode('utf-8')).hexdigest()
    return hash_str
    

def verify_transaction(transaction: dict) -> bool:
    """ 
    トランザクションの signature を検証する
    return: bool
    print: error(BadSignatureError)
    """
    public_key_str = transaction['sender']
    public_key = VerifyingKey.from_string(binascii.unhexlify(public_key_str), curve=SECP256k1)
    # binascii.Error: Odd-length string
    # ecdsa.errors.MalformedPointError
    signature = binascii.unhexlify(transaction['signature'])
    # binascii.Error: Odd-length string
    copy_transaction = transaction.copy()
    copy_transaction.pop('signature')
    try:
        public_key.verify(signature, json.dumps(copy_transaction).encode('utf-8'))
        return True
    except BadSignatureError as e:
        print(e)
        return False
    

def make_thanks_transaction(
        sender_secret_key_str: str, sender_public_key_str: str, 
        receiver_public_key_str: str, MIK: int) -> dict:
    """
    MIK 感謝用トランザクションを作成
    return: dict(keys=['time', 'sender', 'receiver', 'MIK', 'signature'])
    """
    thanks_transaction = {
        'time': datetime.now().isoformat(),
        'sender': sender_public_key_str,
        'receiver': receiver_public_key_str,
        'MIK': MIK,
    }
    sender_secret_key = SigningKey.from_string(
        binascii.unhexlify(sender_secret_key_str), curve=SECP256k1)
    signature = sender_secret_key.sign(
        json.dumps(thanks_transaction).encode('utf-8')).hex()
    thanks_transaction['signature'] = signature
    return thanks_transaction


def make_mikoto_trasaction(receiver_public_key_str: str, MIK: int) -> dict:
    """
    MIK 発行用トランザクションを作成
    return: dict(keys=['time', 'sender', 'receiver', 'MIK', 'signature'])
    sender, signature = 'mikoto_project'
    """
    mikoto_transaction = {
        'time': datetime.now().isoformat(),
        'sender': 'mikoto_project',
        'receiver': receiver_public_key_str,
        'MIK': MIK,
        'signature': 'mikoto_project',
    }
    return mikoto_transaction


def make_key_data() -> dict:
    """ 
    curve: SECP256k1
    return: dict(keys=['secret_key_str', 'public_key_str'])
    """
    secret_key = SigningKey.generate(curve=SECP256k1)
    secret_key_str = secret_key.to_string().hex()
    public_key = secret_key.verifying_key
    public_key_str = public_key.to_string().hex()
    key_data = {
        'secret_key_str': secret_key_str,
        'public_key_str': public_key_str
    }
    return key_data


if __name__ == "__main__":
    # ユーザー情報の辞書を作成
    name_list = ['Dog', 'Cat', 'Lion']
    user_info_dict = {}
    for name in name_list:
        user_info_dict[name] = make_key_data()
    
    transaction_pool = []
    # mikoto_project -> Dog: 100MIK
    transaction_pool.append(
        make_mikoto_trasaction(user_info_dict['Dog']['public_key_str'], 100)
    )
    # Dog -> Cat: 10MIK, Dog -> Lion: 20MIK
    transaction_pool.append(
        make_thanks_transaction(
            user_info_dict['Dog']['secret_key_str'],
            user_info_dict['Dog']['public_key_str'],
            user_info_dict['Cat']['public_key_str'],
            10
        )
    )
    transaction_pool.append(
        make_thanks_transaction(
            user_info_dict['Dog']['secret_key_str'],
            user_info_dict['Dog']['public_key_str'],
            user_info_dict['Lion']['public_key_str'],
            20
        )
    )
    # print('トランザクション・プール')
    # pprint.pprint(transaction_pool, sort_dicts=False)

    for transaction in transaction_pool:
        # 発行したものは検証しない
        if transaction["sender"] == "mikoto_project":
            continue
        else:
            # 検証結果を表示
            # print(verify_transaction(transaction))
            pass
            
    block_chain = make_first_block_chain()
    # print(block_chain)
    sorted_new_block = mining(transaction_pool, block_chain, user_info_dict['Dog']['public_key_str'], 100)
    print('sorted_new_block:')
    pprint.pprint(sorted_new_block, sort_dicts=False)
    
    block_chain.append(sorted_new_block)
    
    print('verify_block_chain:', verify_block_chain(block_chain))
    