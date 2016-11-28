from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.db import models

from .managers import WeChatMemberGroupManager
from .managers import WeChatMemberManager
from .managers import WeChatMenuMatchRuleManager
from .managers import WeChatMenuButtonManager


class WeChatMemberGroup(models.Model):
    group_id = models.IntegerField(verbose_name=_('group id'))
    name = models.CharField(max_length=128, blank=True, verbose_name=_('group name'))
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)

    objects = WeChatMemberGroupManager()

    class Meta:
        app_label = 'wechat'
        verbose_name = _('wechat member group')
        verbose_name_plural = _('wechat member groups')

    def __unicode__(self):
        return self.name


class WeChatMember(models.Model):
    SEX_CHOICES = (
            ('0', _('unknown')),
            ('1', _('male')),
            ('2', _('female')),
            )
    nickname = models.CharField(max_length=128, verbose_name=_('nickname'))
    headimgurl = models.URLField(verbose_name=_('headimgurl'))
    openid = models.CharField(max_length=128, unique=True, verbose_name=_('open id'))
    # unionid = models.CharField(max_length=128, unique=True, verbose_name=_('union id'))
    sex = models.CharField(choices=SEX_CHOICES, max_length=2, default='0', verbose_name=_('sex'))
    city = models.CharField(max_length=128, blank=True, verbose_name=_('city'))
    province = models.CharField(max_length=128, blank=True, verbose_name=_('province'))
    country = models.CharField(max_length=128, blank=True, verbose_name=_('country'))
    subscribe_time = models.DateTimeField(blank=True, verbose_name=_('subscribe_time'))
    remark = models.CharField(max_length=512, blank=True, verbose_name=_('remark'))
    groups = models.ManyToManyField(WeChatMemberGroup, blank=True, verbose_name=_('groups'), related_name='members')
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)

    objects = WeChatMemberManager()

    class Meta:
        app_label = 'wechat'
        verbose_name = _('wechat member')
        verbose_name_plural = _('wechat members')

    def __unicode__(self):
        return self.nickname


class WeChatMenuMatchRule(models.Model):
    KEY_CHOICES = (
            ('group_id', _('group id')),
            ('sex', _('country')),
            ('country', _('country')),
            ('province', _('province')),
            ('city', _('city')),
            ('client_platform_type', _('client platform type')),
            ('language', _('language')),
            )
    key = models.CharField(choices=KEY_CHOICES, max_length=32,  verbose_name=_('rule key'))
    value = models.CharField(max_length=32, verbose_name=_('rule value'))
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)

    objects = WeChatMenuMatchRuleManager()

    class Meta:
        app_label = 'wechat'
        verbose_name = _('wechat menu match rule')
        verbose_name_plural = _('wechat menu match rules')

    def __unicode__(self):
        return '%s: %s' % (self.key, self.value)


class WeChatMenuButton(models.Model):
    TYPE_CHOICES = (
            ('click', _('click')),
            ('view', _('view')),
            )
    menuuid = models.CharField(max_length=32, unique=True, verbose_name=_('menuuid'))
    parent = models.ForeignKey('self', related_name='children', blank=True, verbose_name=_('parent'))
    type = models.CharField(choices=TYPE_CHOICES, max_length=32, verbose_name=_('menu type'))
    name = models.CharField(max_length=40, verbose_name=_('button name'))
    key = models.CharField(max_length=128, blank=True,  verbose_name=_('button key'))
    url = models.URLField(max_length=1024, blank=True,  verbose_name=_('button url'))
    matchrules = models.ManyToManyField(WeChatMenuMatchRule, blank=True, verbose_name=_('matchrules'), related_name='buttons')
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)

    objects = WeChatMenuButtonManager()

    class Meta:
        app_label = 'wechat'
        verbose_name = _('wechat menu button')
        verbose_name_plural = _('wechat menu buttons')

    def __unicode__(self):
        return '%s: %s' % (self.name, self.type)
