from __future__ import unicode_literals

import uuid
from datetime import timedelta
from dateutils import relativedelta
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

import logging
logger = logging.getLogger('tier')


class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False, verbose_name=_('is deleted'))
    dt_created = models.DateTimeField(auto_now_add=True, verbose_name=_('created datetime'))
    dt_updated = models.DateTimeField(auto_now=True, verbose_name=_('updated datetime'))

    class Meta:
        abstract = True

    def delete(self):
        self.is_deleted = True
        self.save()


TIER_SCOPE_CHOICES = (
        ('one year', _('One Year')),
        ('one season', _('One Season')),
        ('one month', _('One Month')),
        ('one day', _('One Day')),
        ('permanent', _('Permanent')),
        )

TIER_SCOPE_EXPIRES_MAP = {
        'one year': relativedelta(years=1),
        'one season': relativedelta(months=3),
        'one month': relativedelta(months=1),
        'one day': relativedelta(days=1),
        'permanent': timedelta.max,
        }

TIER_PACKAGE_CHOICES = (
        ('channel', _('Channel')),
        ('album', _('Album')),
        ('episode', _('Episode')),
        )

class Tier(BaseModel):
    title = models.CharField(max_length=32, verbose_name=_('titer tier'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    message = models.CharField(max_length=32, blank=True, verbose_name=_('tier messagee'))
    remark = models.CharField(max_length=32, blank=True, verbose_name=_('remark'))
    seq = models.IntegerField(default=0, verbose_name=('tier seq'))
    scope = models.CharField(max_length=32, choices=TIER_SCOPE_CHOICES, verbose_name=_('tier scope'))
    package = models.CharField(max_length=32, choices=TIER_PACKAGE_CHOICES, verbose_name=_('tier package'))
    price = models.DecimalField(decimal_places=2, max_digits=9, default=0.0, verbose_name=_('tier price'))
    is_published = models.BooleanField(default=False, verbose_name=_('is published'))

    class Meta:
        app_label = 'term'
        verbose_name = _('tier')
        verbose_name_plural = _('tiers')

    def __unicode__(self):
        scope = filter(lambda x: x[0] == self.scope, TIER_SCOPE_CHOICES)
        scope = scope[0][1] if scope else self.scope
        package = filter(lambda x: x[0] == self.package, TIER_PACKAGE_CHOICES)
        package = package[0][1] if package else self.package
        return '%s x %s, %s' % (scope, package, self.price)


ORDER_STATUS_CHOICES = (
        ('wait-for-payment', _('Wait for Payment')),
        ('succeeded', _('Succeeded')),
        ('failed', _('Faield')),
        ('canceled', _('Canceled')),
        ('expired', _('Expired')),
        )

class Order(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name=_('uuid'))
    tier = models.ForeignKey('Tier', verbose_name=_('tier'))
    scope = models.CharField(max_length=32, choices=TIER_SCOPE_CHOICES, verbose_name=_('tier scope'))
    item = models.IntegerField(default=0, verbose_name=_('order item id'))
    content_type = models.ForeignKey('contenttypes.ContentType', null=True, blank=True, verbose_name=_('content_type'), editable=False)
    item_object = GenericForeignKey('content_type', 'item',)
    package = models.CharField(max_length=32, choices=TIER_PACKAGE_CHOICES, verbose_name=_('tier package'))
    price = models.DecimalField(decimal_places=2, max_digits=9, default=0.0, verbose_name=_('tier price'))
    member = models.ForeignKey('member.Member', related_name='orders', verbose_name = _('member'))
    value = models.DecimalField(decimal_places=2, max_digits=9, default=0.0, verbose_name=_('payment value'))
    status = models.CharField(max_length=32, choices=ORDER_STATUS_CHOICES, verbose_name=_('status'))

    class Meta:
        app_label = 'term'
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def __unicode__(self):
        return 'Order %d' % self.id

    def fill_order(self):
        ct_map = {
                'channel': ContentType.objects.get(model='podcastchannel'),
                'album': ContentType.objects.get(model='podcastalbum'),
                'episode': ContentType.objects.get(model='podcastepisode'),
                }
        self.scope = self.tier.scope if not self.scope else self.scope
        self.package = self.tier.package if not self.package else self.package
        self.content_type = ct_map.get(self.package, None)
        self.price = self.tier.price if not self.price else self.price
        self.value = self.tier.price if not self.value else self.value
        self.status = 'wait-for-payment' if not self.status else self.status

    def save(self, *args, **kwargs):
        if not self.id:
            self.fill_order()
        if not self.item_object:
            # oops
            return
        return super(Order, self).save(*args, **kwargs)

    def check_payment(self, status='succeeded'):
        payments = self.payments.filter(status='succeeded')
        if payments.count() == 1:
            return True
        elif payments.count() > 1:
            logger.warning('Order: %s payments odds!' % self.uuid)
            return True
        else:
            return False

    def make_empty_payment(self, agent='wechat'):
        if self.check_payment():
            return None
        payment = Payment.objects.create(
                order=self,
                status='wait-for-payment',
                agent=agent,
                )
        logger.info('Create payment %s' % payment.uuid)
        return payment

    def make_purchase(self):
        if not self.status == 'succeeded':
            return None
        if not self.item_object:
            return None
        purchase, created = Purchase.objects.get_or_create(
                order=self,
                defaults={
                    'scope': self.scope,
                    'package': self.package,
                    'price': self.price,
                    'content_type': self.content_type,
                    'object_id': self.item,
                    'member': self.member,
                    },
                )
        if created:
            logger.info('Create purchase %s' % purchase.uuid)
        return purchase



PAYMENT_AGENT_CHOICES = (
        ('wechat', _('Wechat')),
        ('invit-conpon', _('Invit-Conpon')),
        )


PAYMENT_STATUS_CHOICES = (
        ('wait-for-payment', _('Wait for Payment')),
        ('succeeded', _('Succeeded')),
        ('failed', _('Faield')),
        )

class Payment(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name=_('uuid'))
    order = models.ForeignKey('Order', related_name='payments', verbose_name=_('order'))
    receipt = models.TextField(blank=True, verbose_name=_('payment receipt'))
    agent = models.CharField(max_length=32, choices=PAYMENT_AGENT_CHOICES, verbose_name=_('payment agent'))
    status = models.CharField(max_length=32, choices=PAYMENT_STATUS_CHOICES, verbose_name=_('status'))

    class Meta:
        app_label = 'term'
        verbose_name = _('payment')
        verbose_name_plural = _('payments')

    def __unicode__(self):
        return 'Payment - %d' % self.id


PURCHASE_CONTENT_TYPE_LIMITS = (
        models.Q(model='podcastchannel', app_label='podcast')
        | models.Q(model='podcastalbum', app_label='podcast')
        | models.Q(model='podcastepisode', app_label='podcast')
        )

class Purchase(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name=_('uuid'))
    scope = models.CharField(max_length=32, choices=TIER_SCOPE_CHOICES, verbose_name=_('tier scope'))
    package = models.CharField(max_length=32, choices=TIER_PACKAGE_CHOICES, verbose_name=_('tier package'))
    price = models.DecimalField(decimal_places=2, max_digits=9, default=0.0, verbose_name=_('tier price'))
    content_type = models.ForeignKey('contenttypes.ContentType', null=True, blank=True, verbose_name=_('content_type'), limit_choices_to=PURCHASE_CONTENT_TYPE_LIMITS)
    object_id = models.PositiveIntegerField(verbose_name=_('object id'), default=0)
    purchase_object = GenericForeignKey('content_type', 'object_id')
    order = models.OneToOneField('Order', verbose_name=_('order'))
    member = models.ForeignKey('member.Member', related_name='purchases', verbose_name=_('member'))
    dt_expired = models.DateTimeField(null=True, verbose_name=_('expired datetime'))
    is_expired = models.BooleanField(default=False, verbose_name=_('is expired'))
    is_permanent = models.BooleanField(default=False, verbose_name=_('is permanent'))

    class Meta:
        app_label = 'term'
        verbose_name = _('ticket')
        verbose_name_plural = _('tickets')

    def __unicode__(self):
        return 'Purchase - %d' % self.order.id

    def save(self, *args, **kwargs):
        if not self.dt_expired and not self.is_permanent:
            tier = self.order.tier
            if tier.scope == 'permanent':
                self.is_permanent = True
            else:
                base_time = self.dt_created or now()
                scope_map = TIER_SCOPE_EXPIRES_MAP
                self.dt_expired = base_time + scope_map.get(
                        tier.scope, relativedelta(0))
        super(Purchase, self).save(*args, **kwargs)
