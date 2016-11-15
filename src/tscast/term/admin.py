from django.contrib import admin
from jet.admin import CompactInline
from django.utils.translation import ugettext_lazy as _



from .models import Tier
from .models import Order
from .models import Payment
from .models import Ticket


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


class TicketModelAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(TicketModelAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


admin.site.register(Tier, TierModelAdmin)
admin.site.register(Order, OrderModelAdmin)
admin.site.register(Payment, PaymentModelAdmin)
admin.site.register(Ticket, TicketModelAdmin)
