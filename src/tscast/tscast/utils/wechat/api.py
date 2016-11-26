import json
import requests
import logging
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


def validate_user(*args, **kwargs):
    avatar = ''
    nickname = ''
    return avatar, nickname

