# -*- coding: utf-8 -*-
import cgi, base64, json
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode


data = [{"a":"123"}]
json = json.dumps(data)


def sign_read_type1(data):
    with open('app_private_key.pem', 'r') as f:
        priKey = f.read().encode()
    rsakey = RSA.importKey(priKey)
    signer = PKCS1_v1_5.new(rsakey) 
    h = SHA256.new(data)
    # h.update(b64decode(json))
    signature = signer.sign(h)
    return b64encode(signature)

def sign_read_type2(data):
    with open('app_private_key.pem', 'r') as f:
        signer = PKCS1_v1_5.new(RSA.importKey(f.read().encode()))
    h = SHA256.new(data)
    # h.update(b64decode(json))
    signature = signer.sign(h)
    return b64encode(signature)

def sign_string(private_key_path, unsigned_string):
    # 开始计算签名
    key = RSA.importKey(open(private_key_path).read())
    signer = PKCS1_v1_5.new(key)
    signature = signer.sign(SHA256.new(unsigned_string.encode("utf8")))
    # base64 编码，转换为unicode表示并移除回车,python2.7中改为encodestring
    sign = base64.encodestring(signature).decode("utf8").replace("\n", "")
    return sign

signed_string = sign_string('app_private_key.pem', "abc\n")    

print ('{"a":"123"}')
print sign_read_type1(json)
print ('a=123, read pem file')
print sign_read_type1('a=123')
print ('a=123, read pem file, with packing')
print sign_read_type2('a=123')
print ('abc\n, read pem file, with packing')
print sign_read_type2('abc\n')
print signed_string  
# def sign(data_file_name, signature_file_name, private_key_file_name):
#   """
#     签名函数使用指定的私钥Key对文件进行签名，并将签名结果写入文件中
#     :param data_file_name: 待签名的数据文件
#     :param signature_file_name: 存放签名结果的文件
#     :param private_key_file_name: 用于签名的私钥文件
#     :return: 签名数据
#     """

#     # 读取待签名数据
#     data_file = open(data_file_name, 'app')