#encoding: utf-8
import urllib
import json
import time
import datetime
from random import Random
import rsa
import binascii
import requests


req_url = "https://api.mch.pospre.com/KsherPay/order_query"

def random_str():
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(32):
        str+=chars[random.randint(0, length)]
    return str

def dh_sign(message):
    """
    签名
    @param message is a dict
    """
    alist=[]
    for key, value in message.items():
        alist.append(key+"="+str(value))
    alist.sort()
    predata = "".join(alist).encode('utf8')

    with open('mch_privkey.pem') as privatefile:
        keydata = privatefile.read()
    dh_privkey = rsa.PrivateKey.load_pkcs1(keydata,'PEM')
    signature = rsa.sign(predata, dh_privkey, 'MD5')
    signature = binascii.hexlify(signature)
    return signature

nonce_str = random_str()

appid = "mch20795"
time_stamp = time.strftime('%Y%m%d%H%M%S')
channel = 'alipay'
mch_order_no = ''
ksher_order_no = '70020190629122845908072'
channel_order_no = ''


dict = {
    'version':'3.0.0',
    'time_stamp':time_stamp,
    'appid': appid,
    'nonce_str': nonce_str,
    'channel': channel,
    'mch_order_no': mch_order_no,
    'ksher_order_no': ksher_order_no,
    'channel_order_no': channel_order_no
}

#签名
signature = dh_sign(dict)
dict.update({'sign': signature})

print json.dumps(dict,sort_keys=True,indent=4)

parmas = urllib.urlencode(dict)
f=urllib.urlopen(req_url,parmas)
response = f.read()


print '请求的数据:\n %s' % json.dumps(dict, sort_keys=True, indent=4)
r = requests.get(req_url, dict)
response_dict = r.json()
print '响应的数据:\n %s' % json.dumps(response_dict, sort_keys=True, indent=4)


if __name__ == '__main__':
    pass
