from django.contrib import admin
from jet.admin import CompactInline
from django.utils.translation import ugettext_lazy as _

from podcast.utils.admin import BaseModelAdmin

from .models import Member
from .models import MemberToken
from .models import SocialNetwork
from .models import PodcastAlbumSubscription
from .models import TrialMember


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

class TrialMemberModelAdmin(BaseModelAdmin):
    list_display = ('user', 'key', 'is_activated', 'dt_created', 'dt_updated', )
    fields = ('key', 'user')
    readonly_fields = ('key', 'is_activated')

admin.site.register(Member, MemberModelAdmin)
admin.site.register(PodcastAlbumSubscription)
admin.site.register(TrialMember, TrialMemberModelAdmin)
