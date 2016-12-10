from django_filters import FilterSet

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response 
from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

from .models import WeChatWxpayNotify
from .models import WeChatWxpayNotifyContent

from .serializers import WeChatWxpayNotifySerializer
from .serializers import WeChatWxpayNotifyContentSerializer

from .parsers import WxPayContentParser


class WeChatWxpayNotifyViewSet(viewsets.ModelViewSet):
    model = WeChatWxpayNotify
    serializer_class = WeChatWxpayNotifySerializer
    authentication_classes = []
    permission_classes =[]
    parser_classes = [WxPayContentParser, ]

    def get_serializer(self, *args, **kwargs):
        '''
        replace the serializer
        '''
        kwargs['context'] = self.get_serializer_context()
        # judge the request content sucess/fail
        request = kwargs['context'].get('request')
        if request and request.method != 'POST':
            return WeChatWxpayNotifySerializer(*args, **kwargs)
        success = kwargs['data'].get('return_code', '') == 'SUCCESS'
        if not success:
            sc = WeChatWxpayNotifySerializer(*args, **kwargs)
        else:
            sc = WeChatWxpayNotifyContentSerializer(*args, **kwargs)
        return sc

    def create(self, *args, **kwargs):
        try:
            res = super(WeChatWxpayNotifyViewSet, self).create(*args, **kwargs)
            content = '<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>'
            status_code = res.status_code
        except Exception as error:
            if hasattr(error, 'detail'):
                error.message = error.detail
            message = error.message
            content = '<xml><return_code><![CDATA[FAIL]]></return_code><return_msg><![CDATA[%s]]></return_msg></xml>' % message
            status_code = 400
        headers = {}
        headers['Content-Type'] = 'application/xml'
        alt_res = Response(content, status=status_code, headers=headers)
        return alt_res


class WeChatWxpayNotifyContentViewSet(viewsets.ModelViewSet):
    model = WeChatWxpayNotifyContent
    serializer_class = WeChatWxpayNotifyContentSerializer

    def is_vlaid(raise_exception=True):
        super

