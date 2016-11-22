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


class PaymentSerializer(serializers.ModelSerializer):
    payload = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = ('agent', 'status', 'payload')

    def get_payload(self, obj):
        if obj.status == 'wait-for-payment':
            return {'prepay_id': 'xxx', 'pay_sign': 'yyy'}
        else:
            return {}


class OrderSerializer(serializers.ModelSerializer):
    from member.models import Member
    # member = serializers.HiddenField(default=Member.objects.get(id=1))
    payments = PaymentSerializer(many=True)

    class Meta:
        model = Order
        fields = ('uuid', 'tier', 'scope', 'item',
                'package', 'price', 'value', 'status',
                'dt_updated', 'dt_created', 'member',
                'payments',
                )
        read_only_fields = ('uuid', 'scope', 'package',
                'price', 'value', 'status',
                'dt_updated', 'dt_created')

    def create(self, validated_data):
        tier = validated_data['tier']
        member = validated_data['member']
        item = validated_data['item']
        ps = validated_data['payments']
        ps = [{'agent': 'wechat'}]
        order = Order.objects.create(
                tier=tier,
                member=member,
                item=item,
                )
        for p in ps:
            agent = p['agent']
            order.make_empty_payment(agent=agent)
        return order


