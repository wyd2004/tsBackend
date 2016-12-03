import json
import requests
import logging
from urllib import urlencode
from urllib import quote as urlquote
from hashlib import sha1
from django.core.cache import cache
from django.core.cache import caches
from django.conf import settings

WECHAT_TOKEN = settings.WECHAT_TOKEN
WECHAT_APPID = settings.WECHAT_APPID
WECHAT_APPSECRET = settings.WECHAT_APPSECRET
# WECHAT_ENCODING_AES_KEY = settings.WECHAT_ENCODING_AES_KEY


logger = logging.getLogger('wechat')


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
