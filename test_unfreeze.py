#encoding: utf-8
import json
import time
from random import Random
import rsa
import binascii
import requests

"""
解冻授权
"""

req_url = "https://api.mch.pospre.com/KsherPayPreAuth/unfreeze"

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
    'mch_request_no': str(int(time.time())),
    'mch_order_no': '',
    'ksher_order_no': '',
    'auth_no': '2019070210002001000283119183',
    'amount': 39000,
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

# 解冻成功异步
{
'app_id': u'2018060601228996', 
'sign': u'rE8nS3nTttvEVcYlH4ER1ZSfTOJTdIv0nC72OVBKFour0oNXW2wEUIa0p+98c3XiLWjP8qldtDxvwgqwp9eEGVgvYuZ3DARCFuf1zqmLaHzgPLvP/fbfRbd14VoQds6NaWYK9P2e6ydAVjDvM2oGVLU6JQ59hGsJ8OM5zcdtyrA=', 
'total_unfreeze_amount': u'500.00', 
'out_order_no': u'60020190621144028500235', 
'charset': u'utf-8', 
'out_request_no': u'RN60020190621144028500235', 
'auth_no': u'2019062110002001000281886861', 
'gmt_create': u'2019-06-21 14:46:06', 
'version': u'1.0', 
'sign_type': u'RSA', 
'total_freeze_amount': u'500.00', 
'auth_app_id': u'2018060601228996', 
'status': u'SUCCESS', 
'total_pay_amount': u'0.00', 
'rest_amount': u'0.00', 
'payer_user_id': u'2088622903359001', 
'gmt_trans': u'2019-06-21 14:46:07', 
'amount': u'500.00', 
'payer_logon_id': u'158****7723', 
'operation_type': u'UNFREEZE', 
'operation_id': u'20190621025153980002', 
'notify_time': u'2019-06-21 14:46:08', 
'notify_id': u'3f4bed0ddfcd9f944fb6f01211ce8e4g02', 
'notify_type': u'fund_auth_unfreeze'
}

if __name__ == '__main__':
    pass

