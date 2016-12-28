# encoding: utf-8

import json
import xmltodict
import requests
import logging
import os
import binascii
from hashlib import md5
from hashlib import sha256

from urllib import urlencode
from urllib import quote as urlquote
from hashlib import sha1
from django.core.cache import cache
from django.core.cache import caches
from django.conf import settings
import time

logger = logging.getLogger('wechat')



WECHAT_TOKEN = settings.WECHAT_TOKEN
WECHAT_APPID = settings.WECHAT_APPID
WECHAT_APPSECRET = settings.WECHAT_APPSECRET
# WECHAT_ENCODING_AES_KEY = settings.WECHAT_ENCODING_AES_KEY


logger = logging.getLogger('wechat')


def cat_xml(kwargs):
    xml = '<xml>\n'
    for k, v in kwargs.items():
        # v = v.encode('utf8')
        # k = k.encode('utf8')
        k = str(k)
        v = str(v)
        xml += '  <' + k + '>' + v + '</' + k + '>\n'
    xml += "</xml>"
    return xml


def decode_wx_xml(xml_str):
    try:
        return xmltodict.parse(xml_str)['xml']
    except Exception as error:
        logger.error(error)
        return {}


def get_access_token(refresh=False):
    '''
    API: https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET
    '''
    access_token = cache.get('wechat_access_token')
    if access_token and not refresh:
        return access_token
    else:
        url = 'https://api.weixin.qq.com/cgi-bin/token'
        params = {
                'grant_type': 'client_credential',
                'appid': WECHAT_APPID,
                'secret': WECHAT_APPSECRET,
                }
        response = requests.get(url, params=params)
        if response.ok:
            data = response.json()
            expires_in = data.get('expires_in')
            access_token = data.get('access_token')
            if access_token and expires_in:
                cache.set('wechat_access_token', access_token, expires_in-100)
                return access_token
            else:
                message = '%s: %s' % (url, json.dumps(response.json()))
                logger.error(message)
        else:
            return None


def validate_wechat_message_nonce(signature, timestamp, nonce, echostr):
    if all((signature, timestamp, nonce, echostr)):
        data = [WECHAT_TOKEN, timestamp, nonce]
        data.sort()
        data = ''.join(data)
        sha1_hash = sha1(data).hexdigest()
        if sha1_hash == signature:
            return echostr
    else:
        return ''


def create_wechat_menu(*button):
    '''
     https://api.weixin.qq.com/cgi-bin/menu/create?access_token=ACCESS_TOKEN
    '''
    url = 'https://api.weixin.qq.com/cgi-bin/menu/create'
    params = {'access_token': get_access_token()}
    data = {'button': button}
    data = json.dumps(data)
    response = requests.post(url, params=params, data=data)
    if response.ok:
        return response.json()
    else:
        return response.content

def get_wechat_oauth_url(redirect_uri, scope='snsapi_userinfo', state='oauth'):
    '''
    https://open.weixin.qq.com/connect/oauth2/authorize?appid=APPID&redirect_uri=REDIRECT_URI&response_type=code&scope=SCOPE&state=STATE#wechat_redirect
    '''
    url = 'https://open.weixin.qq.com/connect/oauth2/authorize'
    redirect_uri = urlquote(redirect_uri, safe='')
    params = {
        'appid': WECHAT_APPID,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': scope,
        'state': state,
        }
    params = urlencode(params)
    anchor = 'wechat_redirect'
    r = '%s?%s#%s' % (url, params, anchor)
    return '%s?%s#%s' % (url, params, anchor)


def get_user_info_access_token(code):
    '''
    https://mp.weixin.qq.com/wiki/9/01f711493b5a02f24b04365ac5d8fd95.html
    https://api.weixin.qq.com/sns/oauth2/access_token?appid=APPID&secret=SECRET&code=CODE&grant_type=authorization_code
    {
        "access_token":"ACCESS_TOKEN",
        "expires_in":7200,
        "refresh_token":"REFRESH_TOKEN",
        "openid":"OPENID",
        "scope":"SCOPE",
        "unionid":"o6_bmasdasdsad6_2sgVt7hMZOPfL"
    }
    '''
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
    params = {
        'appid': WECHAT_APPID,
        'secret': WECHAT_APPSECRET,
        'code': code,
        'grant_type': 'authorization_code',
        }
    response = requests.get(url, params=params)
    if response.ok and 'errcode' not in response.json():
        return response.json()
    else:
        return None


def refresh_user_info_access_token(refresh_token):
    '''
    https://api.weixin.qq.com/sns/oauth2/refresh_token?appid=APPID&grant_type=refresh_token&refresh_token=REFRESH_TOKEN
    '''
    url = 'https://api.weixin.qq.com/sns/oauth2/refresh_token'
    params = {
        'appid': WECHAT_APPID,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
        }
    response = requests.get(url, params=params)
    if response.ok and 'errcode' not in response.json():
        return response.json()
    else:
        return None


def get_user_list(next_openid=None):
    '''
    https://api.weixin.qq.com/cgi-bin/user/get?access_token=ACCESS_TOKEN&next_openid=NEXT_OPENID

    {"total":2,"count":2,"data":{"openid":["","OPENID1","OPENID2"]},"next_openid":"NEXT_OPENID"}
    '''
    url = 'https://api.weixin.qq.com/cgi-bin/user/get'
    params = {'access_token': get_access_token()}
    if next_openid:
        params['next_openid'] = next_openid
    response = requests.get(url, params=params)
    if response.ok:
        return response.json()
    else:
        return None


def get_user_info_by_union_id(union_id):
    '''
    https://api.weixin.qq.com/cgi-bin/user/info?access_token=ACCESS_TOKEN&openid=OPENID&lang=zh_CN

    {
        "subscribe": 1, 
        "openid": "o6_bmjrPTlm6_2sgVt7hMZOPfL2M", 
        "nickname": "Band", 
        "sex": 1, 
        "language": "zh_CN", 
        "city": "广州", 
        "province": "广东", 
        "country": "中国", 
        "headimgurl":    "http://wx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv84eavHiaiceqxibJxCfHe/0", 
       "subscribe_time": 1382694957,
       "unionid": " o6_bmasdasdsad6_2sgVt7hMZOPfL"
       "remark": "",
       "groupid": 0
    }

    '''
    url = 'https://api.weixin.qq.com/cgi-bin/user/info'
    params = {
            'access_token': get_access_token(),
            'openid': union_id,
            'lang': 'zh_CH',
            }
    response = requests.get(url, params=params)
    if response.ok:
        return response.json()
    else:
        return None

def get_user_info(access_token, openid):
    '''
    https://api.weixin.qq.com/sns/userinfo?access_token=ACCESS_TOKEN&openid=OPENID&lang=zh_CN
    {
       "openid":" OPENID",
       "nickname": NICKNAME,
       "sex":"1",
       "province":"PROVINCE"
       "city":"CITY",
       "country":"COUNTRY",
        "headimgurl":    "http://wx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv84eavHiaiceqxibJxCfHe/46", 
            "privilege":[
            "PRIVILEGE1"
            "PRIVILEGE2"
        ],
        "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
    }
    '''
    url = 'https://api.weixin.qq.com/sns/userinfo'
    params = {
        'access_token': access_token,
        'openid': openid,
        'lang': 'zh_CH',
        }
    response = requests.get(url, params=params)
    if response.ok and 'errcode' not in response.json():
        return response.json()
    else:
        return None

def is_user_info_access_token_valid(access_token):
    '''
    https://api.weixin.qq.com/sns/auth?access_token=ACCESS_TOKEN&openid=OPENID
    '''
    url = 'https://api.weixin.qq.com/sns/auth'
    params = {
        'access_token': access_token,
        'openid': openid,
        }
    response = requests.get(url, params=params)
    if response.ok:
        return response.json().get('errmsg') == 'ok'
    else:
        return None

def get_all_groups():
    '''
    https://api.weixin.qq.com/cgi-bin/groups/get?access_token=ACCESS_TOKEN
    '''
    url = 'https://api.weixin.qq.com/cgi-bin/groups/get'
    params = {'access_token': get_access_token()}
    response = requests.post(url, params=params)
    if response.ok:
        return response.json().get('groups')
    else:
        return None

def create_group(name):
    '''
    https://api.weixin.qq.com/cgi-bin/groups/create?access_token=ACCESS_TOKEN
    '''
    url = 'https://api.weixin.qq.com/cgi-bin/groups/create'
    params = {'access_token': get_access_token()}
    data = {'group': {'name': name}}
    data = json.dumps(data)
    response = requests.post(url, params=params, data=data)
    if response.ok:
        return response.json().get('group')
    else:
        return None

def update_group(group_id, name):
    '''
    https://api.weixin.qq.com/cgi-bin/groups/update?access_token=ACCESS_TOKEN
    '''
    url = 'https://api.weixin.qq.com/cgi-bin/groups/update'
    params = {'access_token': get_access_token()}
    data = {'group': {'id': group_id, 'name': name}}
    data = json.dumps(data)
    response = requests.post(url, params=params, data=data)
    if response.ok:
        return response.json().get('errmsg') == 'ok'
    else:
        return None

def delete_group(group_id):
    '''
    https://api.weixin.qq.com/cgi-bin/groups/delete?access_token=ACCESS_TOKEN
    '''
    url = 'https://api.weixin.qq.com/cgi-bin/groups/delete'
    params = {'access_token': get_access_token()}
    data = {'group': {'id': group_id}}
    data = json.dumps(data)
    response = requests.post(url, params=params, data=data)
    if response.ok:
        return response.json().get('errmsg') == 'ok'
    else:
        return None

def query_user_group(openid):
    '''
    https://api.weixin.qq.com/cgi-bin/groups/getid?access_token=ACCESS_TOKEN
    '''
    url = 'https://api.weixin.qq.com/cgi-bin/groups/getid'
    params = {'access_token': get_access_token()}
    data = {'openid': openid}
    data = json.dumps(data)
    response = requests.post(url, params=params, data=data)
    if response.ok:
        return response.json().get('groupid')
    else:
        return None

def update_user_group(openid, to_groupid):
    '''
    https://api.weixin.qq.com/cgi-bin/groups/members/update?access_token=ACCESS_TOKEN
    '''
    url = 'https://api.weixin.qq.com/cgi-bin/groups/members/update'
    params = {'access_token': get_access_token()}
    data = {'openid': openid, 'to_groupid': to_groupid}
    data = json.dumps(data)
    response = requests.post(url, params=params, data=data)
    if response.ok:
        return response.json().get('errmsg') == 'ok'
    else:
        return None

def bulk_update_user_group(openid_list, to_groupid):
    '''
    https://api.weixin.qq.com/cgi-bin/groups/getid?access_token=ACCESS_TOKEN
    '''
    url = 'https://api.weixin.qq.com/cgi-bin/groups/getid'
    params = {'access_token': get_access_token()}
    data = {'openid_list': openid, 'to_groupid': to_groupid}
    data = json.dumps(data)
    response = requests.post(url, params=params, data=data)
    if response.ok:
        return response.json().get('errmsg') == 'ok'
    else:
        return None

def generate_wxpay_sign_md5(kwargs):
    sign_type = 'MD5'
    key = settings.WECHAT_PAYMENT_KEY
    kwargs = {k:v for k, v in kwargs.items() if k}
    ks = sorted(kwargs)
    kw_string = u'&'.join([u'%s=%s' % (k, kwargs[k]) for k in ks])
    kw_string += (u'&key=%s' % key)
    sign = md5(kw_string.encode('utf-8')).hexdigest().upper()
    return (sign_type, sign)

def generate_wxpay_sign_sha256(kwargs):
    sign_type = 'HMAC-SHA256'
    key = settings.WECHAT_PAYMENT_KEY
    kwargs = {k:v for k, v in kwargs.items() if k}
    ks = sorted(kwargs)
    kw_string = u'&'.join([u'%s=%s' % (k, kwargs[k]) for k in ks])
    kw_string += (u'&key=%s' % key)
    sign = sha256(kw_string.encode('utf-8')).hexdigest().upper()
    return (sign_type, sign)


def create_wxpay_prepay(title, attach, order_id, fee, client_ip, product_id, open_id, notify_url, *args, **kwargs):
    '''
    https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_1
    '''
    url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
    # assigned app id
    appid = settings.WECHAT_APPID
    # assigned merchant id
    mch_id = settings.WECHAT_MERCHANT_ID
    # terminal device id
    # set the value to 'WEB' while raised by web page
    device_info = 'WEB'
    # random string, 32 or less characters limits
    nonce_str = binascii.hexlify(os.urandom(20)).decode()
    nonce_str = nonce_str[:32]
    # good description
    body = title 
    # good detail: {'goods_details': [{'goods_id': 'xxx', 
    # 'wxpay_goods_id': 'xxx', 'goods_name': 'xxx',
    # 'quantity': 1, 'price': 21, 'goods_category': 'xxx,
    # 'body': 'xxx'},]}
    detail = None
    # extands information, such as 'haha' 
    attach = attach
    # order id
    out_trade_no = order_id
    # currency type, default CNY
    fee_type = 'CNY'
    # total fee count
    total_fee = fee
    # terminal ip
    spbill_create_ip = client_ip
    # payment created time
    # yyyyMMddHHmmss
    time_start = None
    # payment expire time
    # yyyyMMddHHmmss
    time_expire = None
    # goods tag
    goods_tag = None
    # wechat payment callback url
    notify_url = notify_url
    # trade type, JSAPI, NATIVE, APP
    trade_type = 'JSAPI'
    # product id, local value
    product_id = None
    # specify payment limits
    # such as `no_credit`, means credit is not allowed
    limit_pay = None
    # user open id
    openid = open_id
    # HMAC-SHA256 or MD5, MD5 default
    sign_type = None
    sign = None

    kwargs = {
        'appid': appid,
        'mch_id': mch_id,
        'device_info': device_info,
        'nonce_str': nonce_str,
        'body': body,
        'detail': detail,
        'attach': attach,
        'out_trade_no': out_trade_no,
        'fee_type': fee_type,
        'total_fee': total_fee,
        'spbill_create_ip': spbill_create_ip,
        'time_start': time_start,
        'time_expire': time_expire,
        'goods_tag': goods_tag,
        'notify_url': notify_url,
        'trade_type': trade_type,
        'product_id': product_id,
        'limit_pay': limit_pay,
        'openid': openid,
        'sign_type': 'MD5',
    }
    kwargs = {k:v for k, v in kwargs.items() if v}
    sign_type, sign = generate_wxpay_sign_md5(kwargs)
    kwargs['sign'] = sign
    xml_data = cat_xml(kwargs)
    response = requests.post(url, data=xml_data)
    print response.content
    if not response.ok:
        return None
    res_data = decode_wx_xml(response.content)
    if res_data.get('return_code') != 'SUCCESS':
        return None
    if res_data.get('result_code') != 'SUCCESS':
        return None
    # suppose there is a `prepay_id` in the res_data
    if not res_data.get('prepay_id'):
        return None
    res_sign = res_data['sign']
    del(res_data['sign'])
    check_f, check_sign = generate_wxpay_sign_md5(res_data)
    if res_sign == check_sign:
        pay_sign, timestamp = js_api(res_data)
        res_data['sign'] = pay_sign
        res_data['timestamp'] = timestamp
        return res_data
    else:
        return {}


def parse_wxpay_notification(request, *args, **kwargs):
    '''
    https://pay.weixin.qq.com/wiki/doc/api/app/app.php?chapter=9_7&index=3
    params:
        return_code         String(32)
        return_msg          String(32)
        *appid              String(32) 
        *mch_id             String(32)
         device_info        String(32)
        *nonce_str          String(32)
        *sign               String(32)
        *result_code        String(16)
         err_code           String(32)
         err_code_des       String(128)
        *openid             String(128)
         is_subscribe       String(1)
        *trade_type         String(16)
        *bank_type          String(16)
        *total_fee          Int
         fee_type           String(8)
        *cash_fee           Int
         cash_fee_type      String(16)
         coupon_fee         Int
         coupon_count       Int
         coupon_id_$n       String(20)
         coupon_fee_$n      Int
        *transaction_id     String(32)
        *out_trade_no       String(32)
         attach             String(128)
        *time_end           String(14)
    '''
    body = request.body
    req_data = decode_wx_xml(request.body)
    return req_data


def js_api(js_sign_params):
    """
    生成给JavaScript调用的数据
    详细规则参考 https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=7_7&index=6
    """
    package = "prepay_id={0}".format(js_sign_params["prepay_id"])
    timestamp = int(time.time())
    nonce_str = js_sign_params["nonce_str"]

    js_sign_params = dict(appId=settings.WECHAT_APPID, timeStamp=timestamp,
               nonceStr=nonce_str, package=package, signType="MD5")
    sign_type, sign = generate_wxpay_sign_md5(js_sign_params)
    return sign, timestamp

