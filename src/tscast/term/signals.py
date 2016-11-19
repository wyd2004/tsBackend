from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver



@receiver(post_save, sender='term.Payment')
def change_order_status(sender, instance, created, *args, **kwargs):
    if instance.status == 'succeeded' and instance.order.status=='wait-for-payment':
        instance.order.status = 'succeeded'
        instance.order.make_purchase()
        instance.order.save()

