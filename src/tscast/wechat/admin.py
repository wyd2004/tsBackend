from django.contrib import admin

from jet.admin import CompactInline

from .models import WeChatMemberGroup
from .models import WeChatMember
from .models import WeChatMenuMatchRule
from .models import WeChatMenuButton

from tscast.utils.admin import all_fields


class WeChatMemberGroupModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'group_id', 'name', 'dt_updated', 'dt_updated')
    readonly_fields = all_fields(WeChatMemberGroup)
    has_add_permission = lambda *args: False
    has_delete_permission = lambda *args: False


class WeChatMemberModelAdmin(admin.ModelAdmin):
    search_fields = ('nickname', )
    list_display = ('id', 'openid', 'nickname', 'city', 'province', 'country', 'remark')
    readonly_fields = all_fields(WeChatMember)
    has_add_permission = lambda *args: False
    has_delete_permission = lambda *args: False


class WeChatMenuMatchRuleModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'key', 'value', 'dt_created', 'dt_updated')
    readonly_fields = all_fields(WeChatMenuMatchRule)
    has_add_permission = lambda *args: False
    has_delete_permission = lambda *args: False


class WeChatMenuButtonModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'menuuid', 'name', 'dt_created', 'dt_updated')
    readonly_fields = all_fields(WeChatMenuButton)
    has_add_permission = lambda *args: False
    has_delete_permission = lambda *args: False

#
# admin.site.register(WeChatMemberGroup, WeChatMemberGroupModelAdmin)
# admin.site.register(WeChatMember, WeChatMemberModelAdmin)
# admin.site.register(WeChatMenuMatchRule, WeChatMenuMatchRuleModelAdmin)
# admin.site.register(WeChatMenuButton, WeChatMenuButtonModelAdmin)
