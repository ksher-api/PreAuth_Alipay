#encoding: utf-8
import json
import time
from random import Random
import rsa
import binascii
import requests

"""
APP授权
"""

req_url = "http://api.mch.pospre.com/KsherPayPreAuth/app_freeze"

def random_str():
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(32):
        str+=chars[random.randint(0, length)]
    return str


def ksher_sign(message):
    """
    签名
    @param message is a dict
    """
    alist=[]
    for key, value in message.items():
        alist.append(key+"="+str(value))
    alist.sort()
    predata = "".join(alist).encode('utf8')

    # logger.debug( print_log_name, predata)

    with open('mch_privkey.pem') as privatefile:
        keydata = privatefile.read()
    dh_privkey = rsa.PrivateKey.load_pkcs1(keydata,'PEM')
    signature = rsa.sign(predata, dh_privkey, 'MD5')
    signature = binascii.hexlify(signature)
    return signature



dict = {
    'version': '3.0.0',
    'nonce_str': random_str(),
    'appid': "mch35000",
    'channel': 'alipay',
    'mch_order_no': str(int(time.time())),
    'mch_request_no': str(int(time.time())),
    'amount': 97900,
    'fee_type': 'THB',
    'pay_timeout': '',
    'operator_id': '',
    'notify_url': '',
    'limit_pay': '',
    'device_id': '',
    'payee_logon_id': '',
    'payee_user_id': '',
    'attach': '',
}

#签名
signature = ksher_sign(dict)
dict['sign'] = signature



print '请求的数据:\n %s' % json.dumps(dict, sort_keys=True, indent=4)
r = requests.get(req_url, dict)
response_dict = r.json()
print '响应的数据:\n %s' % json.dumps(response_dict, sort_keys=True, indent=4)

if __name__ == '__main__':
    pass

