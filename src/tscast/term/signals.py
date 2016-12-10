import json
import logging

from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver

logger = logging.getLogger('tscast.term')


@receiver(post_save, sender='term.Payment')
def change_order_status(sender, instance, created, *args, **kwargs):
    if instance.status == 'succeeded' and instance.order.status=='wait-for-payment':
        instance.order.status = 'succeeded'
        instance.order.make_purchase()
        instance.order.save()

@receiver(post_save, sender='wechat.WeChatWxpayNotifyContent')
def wxpay_notify(sender, instance, created, *args, **kwargs):
    if not created:
        return
    out_trade_no = instance.out_trade_no
    try:
        from wechat.serializers import WeChatWxpayNotifySerializer
        from .models import Payment
        payment = Payment.objects.get(uuid=out_trade_no)
        if payment.status in ['succeeded', 'faield']:
            logger.info('payment %s is %s' % (payment.uuid, payment.status))
            return
        if instance.result_code == 'SUCCESS':
            payment.status = 'succeeded'
        elif instance.result_code == 'FAIL':
            payment.status = 'failed'
        notify = WeChatWxpayNotifySerializer(instance=instance)
        try:
            receipt = json.loads(payment.receipt)
            receipt['notify'] = receipt.get('notify', [])
        except:
            receipt = {}
            receipt['notify'] = []
        receipt['notify'].append(notify.data)
        payment.receipt = json.dumps(receipt)
        payment.save()
        logger.info('update payment %s %s' % (
            payment.uuid, payment.status))
    except Exception as error:
        logger.error(error)
