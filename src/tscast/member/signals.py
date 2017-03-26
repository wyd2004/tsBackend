from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import MemberPrivilege
from .models import Privilege
from django.utils.timezone import now
from dateutil import relativedelta
from term.models import TIER_SCOPE_EXPIRES_MAP


@receiver(post_save, sender='term.Purchase')
def update_member_privilege(sender, instance, created, *args, **kwargs):

    purchases = sender.objects.filter(
            member=instance.member,
            is_expired=False,
            is_deleted=False,
            )
    priv = Privilege(purchases)
    priv.expires_datetime = instance.dt_expired
    payload = priv.dumps()
    MemberPrivilege.objects.update_or_create(
            member=instance.member,
            defaults={
                'payload':payload,
                },
            )
