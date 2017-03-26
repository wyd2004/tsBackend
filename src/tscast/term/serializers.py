import json
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.conf import settings

from rest_framework import serializers
from rest_framework.exceptions import NotFound 
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError

from .models import Tier
from .models import Order
from .models import Payment
from .models import Purchase

from member.models import Member, MemberPrivilege
from podcast.models import PodcastChannel
from podcast.models import PodcastAlbum
from podcast.models import PodcastEpisode

from wechat.api import create_wxpay_prepay


class TierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tier
        fields = ('id', 'title', 'description', 'message',
                'seq', 'scope', 'package', 'price')


class PaymentSerializer(serializers.ModelSerializer):
    payload = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = ('agent', 'status', 'payload')

    def get_payload(self, obj):
        if not obj.status == 'wait-for-payment':
            return {}
        try:
            receipt = json.loads(obj.receipt)
            return receipt['prepay']
        except:
            pass
        ip = '127.0.0.1'
        notify_uri = reverse('WeChatWxpayNotifyViewSetPost')
        notify_url = '%s://%s%s' % (
                    settings.SITE_SCHEME,
                    settings.SITE_HOST,
                    notify_uri)
        if self.context.get('request'):
            request = self.context['request']
            ip = request.META.get('REMOTE_ADDR')
        member = obj.order.member
        # memp = MemberPrivilege.objects.filter(member=member)
        # if memp.exists():
        # # truncate previous mem priv.
        #    MemberPrivilege.objects.filter(member=member).delete()
        # # DIRTY
        wechat = member.social_networks.filter(site='wechat').first()
        if wechat:
            open_id = wechat.identifier
        else:
            return {}
        kwargs = {
                'title': obj.order.tier,
                'attach': None,
                # payment uuid
                'order_id': obj.uuid.get_hex(),
                'fee': int(obj.order.value * 100),
                'client_ip': ip,
                'notify_url': notify_url,
                'product_id': obj.order.tier.id,
                'open_id': open_id,
                }
        prepay = create_wxpay_prepay(**kwargs)
        if prepay:
            obj.receipt = json.dumps({'prepay': prepay})
            obj.save()
            return prepay
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
        elif tier.package == 'album':
            model = PodcastAlbum
        elif tier.package == 'episode':
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
            payment = order.make_empty_payment(agent=agent)
        return order
