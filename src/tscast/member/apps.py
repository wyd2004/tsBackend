from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from django.apps import AppConfig



class MemberConfig(AppConfig):
    name = 'member'
    verbose_name = _('member')
    from .signals import update_member_privilege
