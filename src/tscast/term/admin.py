from django.contrib import admin
from jet.admin import CompactInline
from django.utils.translation import ugettext_lazy as _



from .models import Tier
from .models import Order
from .models import Payment
from .models import Purchase


class TierModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'scope', 'package', 'price', 'is_published')
    fields = ('scope', 'package', 'price', 'is_published')
    list_filter = ('scope', 'package', 'is_published')
    list_editable = ('price', 'is_published')

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(TierModelAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid', 'tier', 'member', 'value', 'status')
    readonly_fields = ('status', 'scope', 'package', 'price')

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(OrderModelAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


class PaymentModelAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(PaymentModelAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


class PurchaseModelAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(PurchaseModelAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


admin.site.register(Tier, TierModelAdmin)
admin.site.register(Order, OrderModelAdmin)
admin.site.register(Payment, PaymentModelAdmin)
admin.site.register(Purchase, PurchaseModelAdmin)
