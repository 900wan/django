# -*- coding: utf-8 -*-
import cgi, base64, json
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode


priKey = '''-----BEGIN RSA PRIVATE KEY-----
MIIEwAIBADANBgkqhkiG9w0BAQEFAASCBKowggSmAgEAAoIBAQDDwNIjVIBbQVs8BgEUP85DWRRr5PGdo8pSMxze9JIrSP+vF8Bx0hMlPM4PHOLqe2TZqGHc/1NQGJ+Bxab86WBg/shzLqT83MTJ4VoFaxpRBrox4/22mfWMGxWjT/06J3qMp0ORAIhwrnSRvEn7xPlfyA2BHUqHbtmXvXSkg0Q+ckCIVNg8koBnAGtX6aqPUlfA9jVFcGbpJo+VqFixU05iVw3D6b3K4KEfXp0FruCqWcODv77nHxqa2JBZmXdQtFI/uFC91qcXbwYrIoVeTeyKLotLnUvH9Ox720QGnuMBhlSM4qBYJueC/B/i77n6jMP5xXvUalVQesu76JWvrRLTAgMBAAECggEBALMtyCt2qZbeF/i1Nj+mt9KFs1+fTFoTFppvFrot+62LQB6xCwIkXEn1glfrBPnEwOdKbWmwfD4Qi9BpbxSJOiMOk8R6qaKbIbX4hEH5azlHgx8vpYiDHHOGRyQZj5yvjkk4wWv0pO8fgKv1QXMnNWwq3dGVUibtnFZ8oEwFq23L4iu+tyTSWjJcqs5JxNm50LmJTJHH3Sp4W1qGJDXkOtG2E44As01ZgeTe2KedDEcCA++OefA7PjORRbIovwsD6Pr5lQaRudxM4eNmGU709i9QUoMruNyxRIM+qS65MyHet5PI9qgXkTcAYh9KZyyCKABga624b3cfR7TKlzB8vUECgYEA+whbtk19FKh+7GiB1oIaMdGFJTRZvE2ek43XCda6y3g+8srXYvQfICiALGlV230YmSgDz+aMZK5T4R9cssZwMYL33vWwsd4IFq4+uz1ooWs2TLUbnzUxLjAtg5ux7rdEFJRaTRZCiUlnzJhevYv0idokjffSw6UJ0O9IPgu9EykCgYEAx6Bvypr5FrcNEqoDZEMHqKBqZX1G4HiDkpfqtrVHVxH3Tu8VqS6LOWEcJEen4mv+kAEDbwzo4xiuS8M235jh8NfqlyonJqaJVuWu3oow+jDHuTi2x2w6deqSD+g6FgZHIDFW5ZycLFFvwaaWwyZDVdoD2ZuA3FpqPfPlEQre0ZsCgYEA+ZS3yiqEf3N+rYDCBglYDcvn+rNvvF3XmZBeCfQpx34H59BwEHvyLkDWHlGkARMAz9UO5TaswrTnxF0wBrZweWljE5NmV5EOra4TxIkra8FyPRWbHtD90pQnzD+Rymr/Dw7oMNg+0svenXWoS//H4v61dUi9jbKabdZZFwcItvECgYEAr1pe2LoI08s30I1HLWsz7wv6aewBtmwmJz8LDjNu1y0Q8GVTwakA4wZKkhPfhSUYF6bMPWA5skKb2DFCombJEaaYivCcM3dWbN6VHSaGnz76Mdl/tO187NeANjjnzTD2iXDNxCQti0B9yr1q8UFLJL69YwkVyHojmQgEz1OdJsECgYEA27tc/NfbzM+QvPm0eNOXXUUEeUzAXaIdS4f2QsECOSiLW90PGin5GATIXJegy8JLhEG6IlgUH1Ed18ljJoStbRvE6NPr7woe2q8+wQPeYIgLtCZhrx/9uVxGeTNsLANb9zlMzOLlGDRBHcFIX9Dyz4Iargyc1P2CJfdjWyo7Zew=
-----END RSA PRIVATE KEY-----
'''

data = [{"a":"123"}]
json = json.dumps(data)
def sign(json):
	rsakey = RSA.importKey(priKey)
	signer = PKCS1_v1_5.new(rsakey)
	h = SHA256.new()
	h.update(b64decode(json))
	signature = signer.sign(h)
	return base64.b64encode(signature)
print json

def sign1(json):
	rsakey = RSA.importKey(priKey)
	signer = PKCS1_v1_5.new(rsakey)
	h = SHA256.new()
	h.update(b64decode(json))
	signature = signer.sign(h)
	return b64encode(signature)
print sign(json)
print sign1('a=123')
# def sign(data_file_name, signature_file_name, private_key_file_name):
# 	"""
#     签名函数使用指定的私钥Key对文件进行签名，并将签名结果写入文件中
#     :param data_file_name: 待签名的数据文件
#     :param signature_file_name: 存放签名结果的文件
#     :param private_key_file_name: 用于签名的私钥文件
#     :return: 签名数据
#     """

#     # 读取待签名数据
#     data_file = open(data_file_name, 'app')