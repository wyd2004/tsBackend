from rest_framework import serializers
from rest_framework.exceptions import NotFound 
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Tier
from .models import Order
from .models import Payment
from .models import Purchase

from member.models import Member
from podcast.models import PodcastChannel
from podcast.models import PodcastAlbum
from podcast.models import PodcastEpisode


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


class CurrentMember(object):
    def set_context(self, serializer_field):
        self.member = serializer_field.context['request'].user

    def __call__(self):
        return self.member

class OrderSerializer(serializers.ModelSerializer):
    member = serializers.PrimaryKeyRelatedField(
            read_only=True,
            default=CurrentMember()
            )
    payments = PaymentSerializer(many=True)
    item = serializers.IntegerField(required=True)

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

    def validate(self, v):
        tier = v['tier']
        item = v['item']
        if tier.package == 'channel':
            model = PodcastChannel
        elif iter.package == 'album':
            model = PodcastAlbum
        elif iter.package == 'album':
            model = PodcastEpisode
        if not model.objects.filter(id=item).exists(): 
            raise serializers.ValidationError({'item':_('invalid item')})
        else:
            return v

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
