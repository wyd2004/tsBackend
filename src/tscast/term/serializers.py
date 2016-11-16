from rest_framework import serializers
from rest_framework.exceptions import NotFound 
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError

from .models import Tier
from .models import Order
from .models import Payment
from .models import Purchase

class TierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tier
        fields = ('scope', 'package', 'price')


class OrderSerializer(serializers.ModelSerializer):
    # TODO 
    member = serializers.HiddenField(default=None)
    payment_agent = serializers.SerializerMethodField()
    payment_args = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('uuid', 'tier', 'scope', 'item',
                'package', 'price', 'value', 'status',
                'dt_updated', 'dt_created', 'member',
                'payment_agent', 'payment_args',
                )
        readonly_fields = ('uuid', 'scope', 'package',
                'price', 'value', 'status',
                'dt_updated', 'dt_created')

    def get_payment_agent(self, instance):
        return 'wechat'

    def get_payment_args(self, instance):
        return {}
