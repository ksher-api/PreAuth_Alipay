#encoding: utf-8
import json
import time
from random import Random
import rsa
import binascii
import requests

"""
取消授权
"""

req_url = "https://api.mch.pospre.com/KsherPayPreAuth/cancel_freeze"

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
    'mch_order_no': '',
    'ksher_order_no': '',
    'auth_no': '2019070310002001000283268102',
    'ksher_request_no': '40020190703162939858914',
    'channel_request_no': '',
    'operation_reason': '',
    'notify_url': '',
    'operator_id': '',
    'device_id': '',
    'attach': ''
}

#签名
signature = ksher_sign(dict)
dict['sign'] = signature



print '请求的数据:\n %s' % json.dumps(dict, sort_keys=True, indent=4)
r = requests.get(req_url, dict)
response_dict = r.json()
print '响应的数据:\n %s' % json.dumps(response_dict, sort_keys=True, indent=4)

# 取消成功异步
{
'auth_app_id': u'2018060601228996', 
'notify_type': u'fund_auth_operation_cancel', 
'charset': u'utf-8', 
'app_id': u'2018060601228996', 
'out_request_no': u'RN60020190621145926890798', 
'auth_no': u'2019062110002001000281960821', 
'version': u'1.0', 
'sign_type': u'RSA', 
'action': u'unfreeze', 
'operation_id': u'20190621025731320002', 
'notify_time': u'2019-06-21 15:00:25', 
'sign': u'TJJtNqU6/Ov1aRXwYML/PlwT6aqLdHEonaC3iZ5p+G2H8QMmaHYM2/DVIVrNDl9f4hHQfPUSNsovsy5hWK1ZaiWw4ajGmyTdkpbr0npqWLvTf82Ue53p+7P9HDBTHSPgrKQCzLHTk++VEAmCY0VfB18E1/2KfpA/l09DuArDe4w=', 'notify_id': u'6a883f5c4c59e9b7e82f10a5941fc9dg02', 
'out_order_no': u'60020190621145926890798'
}


"""
请求的数据:
 {
    "appid": "mch35000", 
    "attach": "", 
    "auth_no": "2019070210002001000283119181", 
    "channel": "alipay", 
    "channel_request_no": "", 
    "device_id": "", 
    "ksher_order_no": "", 
    "ksher_request_no": "40020190702160105148013", 
    "mch_order_no": "", 
    "nonce_str": "Bkxus4RVOT2LyAKNHR1wanJc519YEL8x", 
    "notify_url": "", 
    "operation_reason": "", 
    "operator_id": "", 
    "sign": "45917833a48aace12c58ff2bcb9a3a5308947df87f9dd7446b567b4caa5f295f13d7c0636a98e09e0dbf2de209c4192cf64d9c27725cd2ab9f607801a1dc3cc3", 
    "version": "3.0.0"
}
响应的数据:
 {
    "code": 0, 
    "data": {
        "appid": "mch35000", 
        "auth_no": "2019070210002001000283119181", 
        "channel_request_no": "20190702050843240002", 
        "ksher_order_no": "60020190702160105368332", 
        "ksher_request_no": "40020190702160105148013", 
        "mch_order_no": "1562054465", 
        "nonce_str": "Bkxus4RVOT2LyAKNHR1wanJc519YEL8x", 
        "result": "SUCCESS"
    }, 
    "msg": "ok", 
    "sign": "51079d906c432b2e316177fc861292a3ec8af5957d2a6501737f7e3c176c784ab1d933534392dfa9ef8fa739785bfbf678bd87660fa1ef020f5054f9d86086e5", 
    "status_code": "", 
    "status_msg": "", 
    "time_stamp": "", 
    "version": "3.0.0"
}
"""

if __name__ == '__main__':
    pass

