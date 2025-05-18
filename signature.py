import binascii
from ecdsa import SigningKey, VerifyingKey, SECP256k1, BadSignatureError


secret_key = SigningKey.generate(curve=SECP256k1)
public_key = secret_key.verifying_key
secret_key_str = secret_key.to_string().hex()
public_key_str = public_key.to_string().hex()
# print('秘密鍵文字列長：', len(secret_key_str))
# print('秘密鍵文字列：', secret_key_str)
# print('公開鍵文字列長：', len(public_key_str))
# print('公開鍵文字列：', public_key_str)

documents = '文書'
# 電子署名
signature_str = secret_key.sign(documents.encode('utf-8')).hex()
# print('電子署名文字列長：', len(signature_str))
# print('電子署名文字列：', signature_str)

# 文字列から公開鍵と電子署名を復元
public_key = VerifyingKey.from_string(binascii.unhexlify(public_key_str), curve=SECP256k1)
print('公開鍵の型：', type(public_key))
signature = binascii.unhexlify(signature_str)
print('電子署名の型：', type(signature))
# 参考：文字列から秘密鍵を復元
secret_key = SigningKey.from_string(binascii.unhexlify(secret_key_str), curve=SECP256k1)
print('秘密鍵の型：', type(secret_key))

# 改ざん
documents = '文書改'

# 電子署名を検証改
try:
    public_key.verify(signature, documents.encode('utf-8'))
    print("文書は改ざんされていません")
except BadSignatureError as e:
    print("文書が改ざんされています")
    print(e)
