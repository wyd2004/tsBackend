from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(post_save, sender='term.Purchase')
def update_member_privilege(sender, instance, created, *args, **kwargs):
    from .models import MemberPrivilege
    from .models import Privilege

    purchases = sender.objects.filter(
            member=instance.member,
            is_expired=False,
            is_deleted=False,
            )
    payload = Privilege(purchases).dumps()
    terms = Privilege().loads(payload)
    MemberPrivilege.objects.update_or_create(
            member=instance.member,
            defaults={
                'payload':payload,
                },
            )
