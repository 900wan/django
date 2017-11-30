# -*- coding: utf-8 -*-
import cgi, base64, json
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode


ASTRING = [{"a":"123"}]
JSON = json.dumps(ASTRING)
DATA = {
    "out_trade_no": "201601020304",
    "biz_content": {"product": "xxx", "title": "xxx"}
}

print("DATA.items: "+str(DATA.items()))

def ordered_data(data):
    '''没看明白'''
    complex_keys = []
    for key, value in data.items():
        if isinstance(value, dict):
            complex_keys.append(key)

    # 将字典类型的数据单独排序
    for key in complex_keys:
        data[key] = json.dumps(data[key], sort_keys=True).replace(" ", "")

    return sorted([(k, v) for k, v in data.items()])

unsigned_items = ordered_data(DATA)
a = ("{}={}".format(k, v) for k, v in unsigned_items)
print str(a)
unsigned_string = "&".join("{}={}".format(k, v) for k, v in unsigned_items)

def sign_read_type1(data):
    '''计算参数的签名'''
    with open('app_private_key.pem', 'r') as f:
        priKey = f.read().encode()
    rsakey = RSA.importKey(priKey)
    signer = PKCS1_v1_5.new(rsakey) 
    h = SHA256.new(data)
    # h.update(b64decode(json))
    signature = signer.sign(h)
    return b64encode(signature)

def sign_read_type2(data):
    '''计算参数的签名，密钥读取缩减至1行，输出b64'''
    with open('app_private_key.pem', 'r') as f:
        signer = PKCS1_v1_5.new(RSA.importKey(f.read().encode()))
    h = SHA256.new(data)
    signature = signer.sign(h)
    return b64encode(signature)

def sign_read_without_b64en(data):
    '''计算参数的签名，密钥读取缩减至1行，不输出b64'''
    with open('app_private_key.pem', 'r') as f:
        signer = PKCS1_v1_5.new(RSA.importKey(f.read().encode()))
    h = SHA256.new(data)
    signature = signer.sign(h)
    return signature

def sign_string(privateKey_path, unsigned_string):
    # 开始计算签名
    key = RSA.importKey(open(privateKey_path).read())
    signer = PKCS1_v1_5.new(key)
    signature = signer.sign(SHA256.new(unsigned_string.encode("utf8")))
    # base64 编码，转换为unicode表示并移除回车,python2.7中改为encodestring, 感觉这个写法好复杂，为何不能直接用b64encode呢？
    sign = base64.encodestring(signature).decode("utf8").replace("\n", "")
    return sign


def validate_sign(publicKey_path, message, signature):
    with open(publicKey_path, 'r') as f:
        signer = PKCS1_v1_5.new(RSA.importKey(f.read()))
    digest = SHA256.new()
    digest.update(message.encode("utf8"))
    # if signer.verify(digest, base64.decodestring(signature.encode("utf8"))):
    if signer.verify(digest, b64decode(signature)):

        return True
    return False

def show_sign(publicKey_path, message):
    with open(publicKey_path, 'r') as f:
        signer = PKCS1_v1_5.new(RSA.importKey(f.read()))
    digest = SHA256.new()
    # 下面生成摘要
    digest.update(message.encode("utf8"))
    # 下面使用公钥将摘要签名
    signature = signer.sign(digest)
    return signature

signed_string = sign_string('app_private_key.pem', "abc\n")
result = validate_sign('app_public_key.pem', "abc\n", signed_string) 

print ('{"a":"123"}')
print sign_read_type1(JSON)

print ('a=123, sign_read_type1')
print sign_read_type1('a=123')

print ('a=123, sign_read_type2, with packing')
print sign_read_type2('a=123')

print ('"abc\\n", sign_read_type2, with packing')
print sign_read_type2('abc\n')

print ('"abc\\n", sign_read_without_b64en, with packing')
print sign_read_without_b64en('abc\n')

print ('"abc\\n", flzee method, signed_strings')
print sign_string('app_private_key.pem', "abc\n")
print ("Result of validate signature is " + str(result))

print ('show sign, without base64')
print b64encode(show_sign('app_private_key.pem', "abc\n"))

print ("-------* Show the unsigned_items *--------- \n" + str(unsigned_items))
print ('-* Show the unsigned_string *- \n' + str(unsigned_string))
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

# 感谢fzlee的ifconfiger
# 参考http://blog.csdn.net/guyongqiangx/article/details/74454969