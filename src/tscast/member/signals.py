from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender='term.Purchase')
def update_member_privilege(sender, instance, created, *args, **kwargs):
    from .models import MemberPrivilege
    from .models import Privilege

    purchases = sender.objects.filter(
        member=instance.member,
        order = instance.order,
        is_expired=False,
        is_deleted=False,
    )
    priv = Privilege(purchases)
    priv.expires_datetime = instance.dt_expired
    payload = priv.dumps()

    memp = MemberPrivilege.objects.filter(member=instance.order.member)
    if memp.exists():
        old_priv = Privilege()
        old_priv.loads(memp[0].payload)
        if old_priv.episode_ids:
            priv.episode_ids = priv.episode_ids + old_priv.episode_ids
            payload = priv.dumps()

        # update previous mem priv...
        MemberPrivilege.objects.filter(member=instance.order.member).update(
            payload=payload
        )
    else:
        MemberPrivilege.objects.update_or_create(
            member=instance.member,
            defaults={
                'payload':payload,
            },
        )

