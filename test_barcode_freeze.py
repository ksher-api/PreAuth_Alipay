#encoding: utf-8
import json
import time
from random import Random
import rsa
import binascii
import requests


"""

条码授权

"""

req_url = "https://api.mch.pospre.com/KsherPayPreAuth/barcode_freeze"

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


mch_order_no = str(int(time.time()))
dict = {
    'version': '3.0.0',
    'nonce_str': random_str(),
    'appid': "mch35000",
    'channel': 'alipay',
    'mch_order_no': mch_order_no,
    'mch_request_no': 'RN{}'.format(mch_order_no),
    'product': '',
    'pay_timeout': '',
    'payee_logon_id': '',
    'payee_user_id': '',
    'notify_url': '',
    'amount': 99000,
    'fee_type': 'THB',
    'auth_code': '289735853425973816',
    'operator_id': '',
    'device_id': '',
    'limit_pay': ''
}

#签名
signature = ksher_sign(dict)
dict['sign'] = signature



print '请求的数据:\n %s' % json.dumps(dict, sort_keys=True, indent=4)
r = requests.get(req_url, dict)
response_dict = r.json()
print '响应的数据:\n %s' % json.dumps(response_dict, sort_keys=True, indent=4)

# 授权成功异步
{
'app_id': u'2018060601228996', 
'sign': u'AX4l7ZjOEwIrlx8K04TKkh3VVDAcbCtnOAiBQzLZh7uTkCkyIGkRzmYQv8SBrt1ZAyO05ncZuQtuw16T7EboN08Nig03ainSAXadpL4aWfMtYchcK0ES1QGy+PjBbrPp83zKZGgNkey8pw6UBYzX6Of03r+YQMupsOnsSdvvi+w=', 
'total_unfreeze_amount': u'0.00', 
'out_order_no': u'60020190621144028500235', 
'trans_currency': u'THB', 
'charset': u'utf-8', 
'out_request_no': u'RN60020190621144028500235', 
'auth_no': u'2019062110002001000281886861', 
'gmt_create': u'2019-06-21 14:40:28', 
'version': u'1.0', 
'sign_type': u'RSA', 
'total_freeze_amount': u'500.00', 
'auth_app_id': u'2018060601228996', 
'status': u'SUCCESS', 
'total_pay_amount': u'0.00', 
'rest_amount': u'500.00', 
'payer_user_id': u'2088622903359001', 
'gmt_trans': u'2019-06-21 14:40:30', 
'amount': u'500.00', 
'payer_logon_id': u'158****7723', 
'operation_type': u'FREEZE', 
'operation_id': u'20190621025153970002', 
'notify_time': u'2019-06-21 14:40:30', 
'notify_id': u'ae9dc7b44e2923a8cba50681c832803g02', 
'notify_type': u'fund_auth_freeze'
}

"""
请求的数据:
 {
    "amount": 99000, 
    "appid": "mch35000", 
    "auth_code": "289749253439974256", 
    "channel": "alipay", 
    "device_id": "", 
    "fee_type": "THB", 
    "limit_pay": "", 
    "mch_order_no": "1562054465", 
    "mch_request_no": "RN1562054465", 
    "nonce_str": "KlY7OFYGzk0byzg49ts90GhXFBgETnOe", 
    "notify_url": "", 
    "operator_id": "", 
    "pay_timeout": "", 
    "payee_logon_id": "", 
    "payee_user_id": "", 
    "product": "", 
    "sign": "1608c0705b36997d30545232d7a4ecfc17016dee5dfe38318af904d9c45aae441e3cf280f0cc9d931db6e167017f521324f36a64d75972c92e57add35588c79b", 
    "version": "3.0.0"
}
响应的数据:
 {
    "code": 0, 
    "data": {
        "amount": 99000, 
        "appid": "mch35000", 
        "attach": "", 
        "auth_no": "2019070210002001000283119181", 
        "channel": "alipay", 
        "channel_request_no": "20190702050843240002", 
        "device_id": "", 
        "fee_type": "THB", 
        "ksher_order_no": "60020190702160105368332", 
        "ksher_request_no": "40020190702160105148013", 
        "local_create_time": "", 
        "local_expire_time": "2019-08-01 15:01:08", 
        "local_trans_time": "2019-07-02 15:01:08", 
        "mch_order_no": "1562054465", 
        "nonce_str": "KlY7OFYGzk0byzg49ts90GhXFBgETnOe", 
        "operation_type": "AUTH-FREEZE", 
        "operator_id": "10698", 
        "rest_amount": 99000, 
        "result": "SUCCESS", 
        "source_no": "289749253439974256", 
        "total_freeze_amount": 99000, 
        "total_pay_amount": 0
    }, 
    "msg": "ok", 
    "sign": "442e459c353d164efe28ae1270dc543e96989938be88f17ab6fd4fea90dbef3f718c48c5b9b58a0ac00674fdb4fdb2395d54f7412827b4c716d2fd70d160233b", 
    "status_code": "", 
    "status_msg": "", 
    "time_stamp": "", 
    "version": "3.0.0"
}
"""


if __name__ == '__main__':
    pass


# 20000 记为FAIL
