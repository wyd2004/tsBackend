from __future__ import unicode_literals

import pytz
import logging

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.utils.datetime_safe import datetime

from .managers import WeChatMemberGroupManager
from .managers import WeChatMemberManager
from .managers import WeChatMenuMatchRuleManager
from .managers import WeChatMenuButtonManager

from .api import get_user_list
from .api import get_user_info_by_union_id
from .api import get_all_groups

tz = pytz.timezone(settings.TIME_ZONE)

dt = lambda stamp: datetime.fromtimestamp(stamp, tz)

logger = logging.getLogger('wechat')


class WeChatMemberGroup(models.Model):
    group_id = models.IntegerField(verbose_name=_('group id'))
    name = models.CharField(max_length=128, blank=True, verbose_name=_('group name'))
    count = models.IntegerField(default=0, verbose_name=_('user count'))
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)

    objects = WeChatMemberGroupManager()

    class Meta:
        app_label = 'wechat'
        verbose_name = _('wechat member group')
        verbose_name_plural = _('wechat member groups')

    def __unicode__(self):
        return self.name

def fetch_wechat_groups():
    data = get_all_groups() or []
    for group in data:
        g, c = WeChatMemberGroup.objects.update_or_create(
                group_id=group['id'],
                defaults={
                    'name': group['name'],
                    'count': group['count'],
                    },
                )
        c = 'create' if c else 'update'
        logger.info('%s %s %s' % (c, group['id'], group['name']))




class WeChatMember(models.Model):
    SEX_CHOICES = (
            ('0', _('unknown')),
            ('1', _('male')),
            ('2', _('female')),
            )
    SUBSCRIBE_CHOICES = (
            ('0', _('No')),
            ('1', _('Yes')),
            )
    subscribe = models.CharField(choices=SUBSCRIBE_CHOICES,max_length=3, default='0', verbose_name=_('subscribe'))
    nickname = models.CharField(max_length=128, blank=True, verbose_name=_('nickname'))
    headimgurl = models.URLField(blank=True, verbose_name=_('headimgurl'))
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

def fetch_wechat_member_list():
    has_next = True
    next_openid = None
    total = -1
    sum_count = 0
    while has_next:
        data = get_user_list(next_openid)
        if not data:
            has_next = False
        if 'total' in data:
            total = data['total']
        if 'next_openid' in data:
            next_openid = data['next_openid']
        if 'data' in data:
            openids = data['data'].get('openid',[])
            for open_id in openids:
                sum_count += 1
                logger.info('get openid %s' % open_id)
                yield open_id
        if sum_count == total:
            has_next = False


def fetch_wechat_members():
    for open_id in fetch_wechat_member_list():
        data = get_user_info_by_union_id(open_id) or {}
        if 'openid' in data:
            member, created = WeChatMember.objects.update_or_create(
                openid=data['openid'],
                defaults={
                    'subscribe': data.get('subscribe'),
                    'nickname': data.get('nickname'),
                    'headimgurl': data.get('headimgurl'),
                    'sex': data.get('sex'),
                    'city': data.get('city'),
                    'province': data.get('province'),
                    'country': data.get('country'),
                    'subscribe_time': dt(data.get('subscribe_time')) if data.get('subscribe_time') else '',
                    'remark': data.get('remark'),
                    # 'groups': ,
                    }
                )
            create = 'create' if created else 'update'
            logger.info('%s %s: %s' % (
                create,
                data.get('openid'),
                data.get('nickname'),
                ))


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


class WeChatWxpayNotify(models.Model):
    return_code = models.CharField(max_length=16, verbose_name=_('return_code'))
    return_msg = models.CharField(max_length=128, blank=True, verbose_name=_('return_msg'))
    dt_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'wechat'
        verbose_name = _('wechat wxpay notify')
        verbose_name_plural = _('wechat wxpay notifies')

    def __unicode__(self):
        return self.return_msg


class WeChatWxpayNotifyContent(WeChatWxpayNotify):
    '''
    https://pay.weixin.qq.com/wiki/doc/api/app/app.php?chapter=9_7&index=3
    params:
        return_code         String(16)
        return_msg          String(128)
        *appid              String(32) 
        *mch_id             String(32)
         device_info        String(32)
        *nonce_str          String(32)
        *sign               String(32)
        *result_code        String(16)
         err_code           String(32)
         err_code_des       String(128)
        *openid             String(128)
         is_subscribe       String(1)
        *trade_type         String(16)
        *bank_type          String(16)
        *total_fee          Int
         fee_type           String(8)
        *cash_fee           Int
         cash_fee_type      String(16)
         coupon_fee         Int
         coupon_count       Int
         coupon_id_$n       String(20)
         coupon_fee_$n      Int
        *transaction_id     String(32)
        *out_trade_no       String(32)
         attach             String(128)
        *time_end           String(14)
    '''
    # return_code         String(32)
    # return_msg          String(32)
    appid = models.CharField(max_length=32,verbose_name=_('appid'))
    mch_id = models.CharField(max_length=32, verbose_name=_('mch_id'))
    device = models.CharField(max_length=32, blank=True, verbose_name=_('mch_id'))
    nonce_str = models.CharField(max_length=32, verbose_name=_('nonce_str'))
    sign = models.CharField(max_length=32, verbose_name=_('sign'))
    result_code = models.CharField(max_length=16, verbose_name=_('result_code'))
    err_code = models.CharField(max_length=32, blank=True, verbose_name=_('err_code'))
    err_code_des = models.CharField(max_length=128, blank=True, verbose_name=_('err_code_des'))
    openid = models.CharField(max_length=128, verbose_name=_('openid'))
    is_subscribe = models.CharField(max_length=1, blank=True, verbose_name=_('is_subscribe'))
    trade_type = models.CharField(max_length=16, verbose_name=_('trade_type'))
    bank_type = models.CharField(max_length=16, verbose_name=_('bank_type'))
    total_fee = models.IntegerField(verbose_name=_('total_fee'))
    fee_type = models.CharField(max_length=8, blank=True, verbose_name=_('fee_type'))
    cash_fee = models.IntegerField(null=True, blank=True, verbose_name=_('cash_fee'))
    cash_fee_type = models.CharField(max_length=18, blank=True, verbose_name=_('cash_fee_type'))
    coupon_fee = models.IntegerField(null=True, blank=True, verbose_name=_('coupon_fee'))
    coupon_count = models.IntegerField(null=True, blank=True, verbose_name=_('coupon_count'))
    coupon_id_n = models.TextField(blank=True, verbose_name=_('coupon_id_n'))
    coupon_fee_n = models.TextField(blank=True, verbose_name=_('coupon_fee_n'))
    transaction_id = models.CharField(max_length=32, verbose_name=_('transaction_id'))
    out_trade_no = models.CharField(max_length=32, verbose_name=_('out_trade_no'))
    attach = models.CharField(max_length=128, blank=True, verbose_name=_('attach'))
    time_end = models.CharField(max_length=14, verbose_name=_('time_end'))


    class Meta:
        app_label = 'wechat'
        verbose_name = _('wechat wxpay notify')
        verbose_name_plural = _('wechat wxpay notifies')

    def __unicode__(self):
        return self.out_trade_no
