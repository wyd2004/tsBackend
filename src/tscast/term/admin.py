from django.contrib import admin
from jet.admin import CompactInline
from django.utils.translation import ugettext_lazy as _


from .models import Tier
from .models import Order
from .models import Payment
from .models import Purchase


class TierModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'seq',  'scope', 'package', 'price', 'is_published')
    fields = ('title', 'description', 'message', 'remark', 'seq', 'scope', 'package', 'price', 'is_published')
    list_filter = ('title', 'seq', 'scope', 'package', 'is_published')
    list_editable = ('price', 'is_published')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        actions = super(TierModelAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

class PaymentInline(CompactInline):
    model = Payment
    exclude = ('is_deleted',)
    readonly_fields = ('receipt', 'agent', 'status')
    fields = ('agent', 'receipt', 'status')
    extra = 0

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


class PurchaseInline(CompactInline):
    model = Purchase
    exclude = ('is_deleted',)
    readonly_fields = ('package', 'scope', 'content_type', 'object_id', 'purchase_object', 'member', 'order',) 
    fields = ('package', 'scope',
            # 'content_type', 'object_id',
            'purchase_object', 'member', 'order',)
    extra = 0

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'scope', 'package', 'item_object', 'member', 'price',  'value', 'status')
    readonly_fields = ('tier', 'member', 'status', 'scope', 'item_object', 'package', 'price', 'value')
    exclude = ('is_deleted',)
    fields = ('tier', 'item_object',
            'member', 'status',
            # 'package', 'scope',
            'price', 'value')
    list_filter = ('status', 'tier__scope', 'tier__package')
    search_fields = ('order__member__username',)
    inlines = (PaymentInline, PurchaseInline)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def get_actions(self, request):
        actions = super(OrderModelAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def item_object(self, obj):
        return obj.item_object
    item_object.short_description = _('item object')


class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'agent', 'status')
    list_filter = ('status', 'agent')
    search_fields = ('order__member__username',)
    readonly_fields = ('order', 'receipt', 'agent', 'status')
    exclude = ('is_deleted',)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(PaymentModelAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


class PurchaseModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'member', 'scope', 'package', 'purchase_object', 'is_expired', 'dt_expired', 'is_permanent')
    list_filter = ('order__tier__scope', 'order__tier__package')
    search_fields = ('member__username',)
    readonly_fields = ( 'order', 'member', 'scope', 'package', 'price', 'purchase_object', 'is_expired', 'dt_expired', 'is_permanent')
    exclude = ('is_deleted', 'object_id', 'content_type',)


    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(PurchaseModelAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


admin.site.register(Tier, TierModelAdmin)
admin.site.register(Order, OrderModelAdmin)
admin.site.register(Payment, PaymentModelAdmin)
admin.site.register(Purchase, PurchaseModelAdmin)
