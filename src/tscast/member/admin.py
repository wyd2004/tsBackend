from django.contrib import admin
from jet.admin import CompactInline
from django.utils.translation import ugettext_lazy as _

from podcast.utils.admin import BaseModelAdmin

from .models import Member
from .models import MemberToken
from .models import SocialNetwork
from .models import PodcastAlbumSubscription
from .models import MemberInvitation 


class PodcastAlbumSubscriptionInline(CompactInline):
    model = PodcastAlbumSubscription
    extra = 0

class SocialNetworkInline(CompactInline):
    model = SocialNetwork
    extra = 0

class MemberTokenInline(CompactInline):
    model = MemberToken
    extra = 0

class MemberModelAdmin(BaseModelAdmin):
    list_display = ('id', 'username', 'nickname', 'avatar', 'dt_updated', )
    fields = ('username', 'nickname', 'avatar')
    inlines = (
            PodcastAlbumSubscriptionInline,
            SocialNetworkInline,
            MemberTokenInline,
            )

    def has_delete_permission(self, request, obj=None):
        return False


class MemberInvitationModelAdmin(BaseModelAdmin):
    list_display = ('id', 'key', 'user', 'is_activated', 'dt_created', 'remark', )
    search_fields = ('remark',)
    list_filter = ('is_activated',)
    fields = ('key', 'user', 'is_activated', 'dt_created', 'dt_updated', 'remark')
    readonly_fields = ('key', 'user', 'is_activated', 'dt_created', 'dt_updated')
    change_list_template = "change_list.html"

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_bulk_add_permission(self, request):
        return True


class PodcastAlbumSubscriptionModelAdmin(BaseModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

admin.site.register(Member, MemberModelAdmin)
admin.site.register(PodcastAlbumSubscription, PodcastAlbumSubscriptionModelAdmin)
admin.site.register(MemberInvitation, MemberInvitationModelAdmin)
