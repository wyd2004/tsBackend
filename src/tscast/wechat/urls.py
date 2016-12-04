from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin


from .views import wechat_message

urlpatterns = [
    url(r'^wechat/message/', wechat_message),
]
