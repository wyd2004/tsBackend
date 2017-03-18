import io
import qrcode
import base64
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.urls import reverse as url_reverse
from django.conf import settings

from jet.admin import CompactInline
from podcast.utils.admin import BaseModelAdmin

from .models import Member
from .models import MemberToken
from .models import MemberPrivilege
from .models import SocialNetwork
from .models import PodcastAlbumSubscription
from .models import MemberInvitation 


class PodcastAlbumSubscriptionInline(CompactInline):
    model = PodcastAlbumSubscription
    extra = 0
    exclude = ('is_deleted',)
    readonly_fields = ('album',)

class SocialNetworkInline(CompactInline):
    model = SocialNetwork
    extra = 0
    readonly_fields = ('site', 'identifier', 'avatar', 'nickname')

class MemberTokenInline(CompactInline):
    model = MemberToken
    extra = 0

class MemberPrivilegeInline(CompactInline):
    exclude = ('is_deleted',)
    readonly_fields = ('payload',)
    model = MemberPrivilege
    max_num = 0
    extra = 0

    def has_add_permission(self, request):
        return False

class MemberModelAdmin(BaseModelAdmin):
    list_display = ('id', 'username', 'nickname', 'avatar', 'dt_updated', )
    search_fields = ('member__nickname')
    fields = ('username', 'nickname', 'avatar')
    readonly_fields = ('username', 'nickname', 'avatar')
    inlines = (
            MemberPrivilegeInline,
            PodcastAlbumSubscriptionInline,
            SocialNetworkInline,
            MemberTokenInline,
            )

    def has_delete_permission(self, request, obj=None):
        return False


class URLOutput(forms.widgets.Input):
    def render(self, name, value, attrs=None):
        return '<p>%s</p>' % value

class ImageOutput(forms.widgets.Input):
    def render(self, name, value, attrs=None):
        return u'<img alt="Embedded Image" src="data:image/png;base64, %s"/>' % value


class MemberInvitationForm(forms.ModelForm):
    url = forms.Field(label=_('URL'), disabled=False, widget=URLOutput, required=False)
    qr = forms.Field(label=_('QRCode'), disabled=False, widget=ImageOutput, required=False)

    class Meta:
        model = MemberInvitation
        exclude = ('is_deleted',)
        order_fields = ('key', 'url', 'qr', 'user', 'is_activated', 'remark')

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            instance = kwargs['instance']
            if not 'initial' in kwargs:
                kwargs['initial'] = {}
            url = '%s://%s%s' % (
                    settings.SITE_SCHEME,
                    settings.SITE_HOST,
                    url_reverse('api:invitation-activate', kwargs={'key': instance.key})
                    )
            kwargs['initial']['url'] = url
            qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=4, border=1)
            qr.add_data(url)
            qr.make(fit=True)
            image = qr.make_image()
            bio = io.BytesIO()
            image.save(bio)
            b64 = base64.b64encode(bio.getvalue())
            kwargs['initial']['qr'] = b64
        super(MemberInvitationForm, self).__init__(*args, **kwargs)



class MemberInvitationModelAdmin(BaseModelAdmin):
    form = MemberInvitationForm
    list_display = ('id', 'key', 'user', 'is_activated', 'dt_created', 'remark', )
    search_fields = ('remark',)
    list_filter = ('is_activated',)
    # fields = ('key', 'user', 'is_activated', 'dt_created', 'dt_updated', 'remark')
    readonly_fields = ('key', 'user', 'is_activated', 'dt_created', 'dt_updated')
    change_list_template = "change_list.html"

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_bulk_add_permission(self, request):
        return True


class PodcastAlbumSubscriptionModelAdmin(BaseModelAdmin):
    list_display = ('id', 'album', 'member')
    search_fields = ('member__username', 'member__nickname')
    list_filter = ('album',)
    readonly_fields = ('album', 'member')
    exclude = ('is_deleted', )
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

class MemberPrivilegeModelAdmin(BaseModelAdmin):
    pass

admin.site.register(Member, MemberModelAdmin)
# admin.site.register(MemberPrivilege)
admin.site.register(PodcastAlbumSubscription, PodcastAlbumSubscriptionModelAdmin)
# admin.site.register(MemberInvitation, MemberInvitationModelAdmin)

