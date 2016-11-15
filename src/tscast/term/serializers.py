from rest_framework import serializers
from rest_framework.exceptions import NotFound 
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError

from .models import Tier

class TierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tier
        fields = ('scope', 'package', 'price')
