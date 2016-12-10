from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin


from rest_framework import routers

from .views import wechat_message
from .viewsets import WeChatWxpayNotifyViewSet
from .viewsets import WeChatWxpayNotifyContentViewSet



urlpatterns = [
        url(r'^wechat/message/', wechat_message),
        url(r'^wechat/wxpay/notify/', WeChatWxpayNotifyViewSet.as_view({'post': 'create'}), name='WeChatWxpayNotifyViewSetPost'),
        ]
