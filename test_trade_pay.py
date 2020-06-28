#encoding: utf-8

import json
import time
from random import Random
import rsa
import binascii
import requests


"""
授权支付

"""


req_url = "https://api.mch.pospre.com/KsherPayPreAuth/trade_pay"

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
    'auth_no': '2019070210002001000283179746',
    'total_fee': 1800,
    'fee_type': 'THB',
    'product': 'AUTH_PAY_TEST',
    'pay_timeout': '',
    'auth_confirm_mode': '',
    'notify_url': '',
    'operator_id': '',
    'device_id': '',
    'attach': ''
}

#签名
signature = ksher_sign(dict)
dict['sign'] = signature



print('请求的数据:\n %s' % json.dumps(dict, sort_keys=True, indent=4))

r = requests.get(req_url,dict)

response_dict = r.json()
print('响应的数据:\n %s' % json.dumps(response_dict, sort_keys=True, indent=4))

if __name__ == '__main__':
    pass

