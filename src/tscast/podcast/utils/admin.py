from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.db import models
from django.utils.safestring import mark_safe

class AdminImageWidget(forms.FileInput):
    """
    A ImageField Widget for admin that shows a thumbnail.
    """

    def __init__(self, attrs={}):
        super(AdminImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            output.append(('<a target="_blank" href="%s">'
                           '<img src="%s" style="height: 28px;" /></a> '
                           % (value.url, value.url)))
        output.append(super(AdminImageWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))


class BaseModelAdmin(admin.ModelAdmin):
    empty_value_display = _('Waiting for full fill.') 
    formfield_overrides = {
            models.ImageField: {'widget': AdminImageWidget},
        }
    list_per_page = 20

    def get_queryset(self, request):
        qs = super(admin.ModelAdmin, self).get_queryset(request)
        fields = [field.name for field in qs.model._meta.fields]
        if 'is_deleted' in fields:
            qs = qs.filter(is_deleted=False)
        return qs

    actions=['bulk_delete_selected']

    def get_actions(self, request):
        actions = super(BaseModelAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def bulk_delete_selected(self, request, queryset):
        if 'is_deleted' in (f.name for f in queryset.model._meta.fields):
            queryset.update(is_deleted=True)
        else:
            for obj in queryset:
                obj.delete()
        self.message_user(request, '%s' % _('successfully deleted'))
    bulk_delete_selected.short_description = _('delete selected')
