import json
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.conf import settings

from rest_framework import serializers
from rest_framework.exceptions import NotFound 
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError

from .models import WeChatWxpayNotify
from .models import WeChatWxpayNotifyContent


class WeChatWxpayNotifySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeChatWxpayNotify


class WeChatWxpayNotifyContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeChatWxpayNotifyContent


