from hashlib import sha1
from django.core.cache import cache
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from django.http.response import HttpResponse
from django.http.response import HttpResponseNotFound
from .api import validate_wechat_message_nonce

@csrf_exempt
def wechat_message(request):
    signature = request.GET.get('signature')
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')
    echostr = request.GET.get('echostr')
    if all((signature, timestamp, nonce, echostr)):
        echo = validate_wechat_message_nonce(signature, timestamp, nonce, echostr)
        if echo:
            return HttpResponse(echostr)
        else:
            return HttpResponse()
    else:
        return HttpResponse()


def validate_user(*args, **kwargs):
    avatar = ''
    nickname = ''
    return avatar, nickname

@csrf_exempt
def wechat_oauth_callback(request):
    return HttpResponse()

