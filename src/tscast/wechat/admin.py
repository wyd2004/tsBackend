from django.contrib import admin

from jet.admin import CompactInline

from .models import WeChatMemberGroup
from .models import WeChatMember
from .models import WeChatMenuMatchRule
from .models import WeChatMenuButton


class WeChatMemberGroupModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'group_id', 'name', 'dt_updated', 'dt_updated')


class WeChatMemberModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'nickname', 'city', 'province', 'country', 'remark')


class WeChatMenuMatchRuleModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'key', 'value', 'dt_created', 'dt_updated')


class WeChatMenuButtonModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'menuuid', 'name', 'dt_created', 'dt_updated')


admin.site.register(WeChatMemberGroup, WeChatMemberGroupModelAdmin)
admin.site.register(WeChatMember, WeChatMemberModelAdmin)
admin.site.register(WeChatMenuMatchRule, WeChatMenuMatchRuleModelAdmin)
admin.site.register(WeChatMenuButton, WeChatMenuButtonModelAdmin)
