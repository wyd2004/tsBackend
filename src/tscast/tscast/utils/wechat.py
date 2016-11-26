from hashlib import sha1
from django.core.cache import cache
from django.conf import settings
from django.http.response import HttpResponse
from django.http.response import HttpResponseNotFound

WECHAT_TOKEN = settings.WECHAT_TOKEN
WECHAT_ENCODING_AES_KEY = settings.WECHAT_TOKEN # TODO

def wechat_message(request):
    signature = request.GET.get('signature')
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')
    echostr = request.GET.get('echostr')
    if not all((signature, timestamp, nonce, echostr)):
        return HttpResponseNotFound()
    data = [WECHAT_TOKEN, timestamp, nonce]
    data.sort()
    data = ''.join(data)
    sha1_hash = sha1(data).hexdigest()
    if sha1_hash == signature:
        return HttpResponse(echostr)
    else:
        return HttpResponseNotFound()


def validate_user(*args, **kwargs):
    avatar = ''
    nickname = ''
    return avatar, nickname
