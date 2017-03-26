from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.timezone import now


@receiver(post_save, sender='term.Purchase')
def update_member_privilege(sender, instance, created, *args, **kwargs):
    from .models import MemberPrivilege
    from .models import Privilege

    purchases = sender.objects.filter(
            member=instance.member,
            is_expired=False,
            is_deleted=False,
            ).order_by("-dt_expired")
    priv = Privilege(purchases)
    memp = MemberPrivilege.objects.filter( member=instance.member)
    if memp.exists():
        # after pay money,update priv data before.
        exp_time = purchases[0].dt_expired
        priv.expires_datetime = exp_time
    payload = priv.dumps()
    # terms = Privilege().loads(payload)
    MemberPrivilege.objects.update_or_create(
            member=instance.member,
            defaults={
                'payload':payload,
                },
            )
