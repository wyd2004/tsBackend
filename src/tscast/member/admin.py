from django.contrib import admin
from jet.admin import CompactInline
from django.utils.translation import ugettext_lazy as _

from podcast.utils.admin import BaseModelAdmin

from .models import Member
from .models import MemberToken
from .models import SocialNetwork
from .models import PodcastAlbumSubscription


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
    display_list = ('id', 'username', 'nickname', 'avatar', 'dt_updated', )
    fields = ('username', 'nickname', 'avatar')
    inlines = (
            PodcastAlbumSubscriptionInline,
            SocialNetworkInline,
            MemberTokenInline,
            )


admin.site.register(Member, MemberModelAdmin)
