from django.contrib import admin
from jet.admin import CompactInline
from django.utils.translation import ugettext_lazy as _

from .utils.admin import BaseModelAdmin
from .models import PodcastChannel
from .models import PodcastHost
from .models import PodcastAlbum
from .models import PodcastEpisode
# from .models import PodcastEnclosure


# class PodcastEnclosureInline(CompactInline):
#     model = PodcastEnclosure
#     extra = 0
#     readonly_fields = ('length', 'size')
#     exclude = ('is_deleted',)
#     fields = ('title', 
#             'expression', 'file', 'file_url',
#             'size', 'length',
#             )
#     show_change_link = True


class PodcastEpisodeInline(CompactInline):
    model = PodcastEpisode
    # prepopulated_fields = {"slug": ("title",)}
    extra = 0
    exclude = ('is_deleted',)
    fields = ('title', 'subtitle', 'serial', 'image', 'copyright', 'status',
            'hosts', 'explicit', 'keywords', 'description',
            )


class PodcastAlbumInline(CompactInline):
    model = PodcastAlbum
    extra = 0
    exclude = ('is_deleted',)


class PodcastChannelAdmin(BaseModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('id', 'name', 'slug', 'image',)
    exclude = ('is_deleted',)
    search_fields = ('name',)
    fields = ('name', 'slug', 'image', 'description')


class PodcastHostAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'short_description', 'albums_count', 'episodes_count', 'dt_updated')
    search_fields = ('name',)
    fieldsets = (
        (None, {
            'fields': ('channel', 'name', 'image', 'description',)
                }),
        )
    # ordering = ('name', 'dt_updated')
    exclude = ('is_deleted',)

    def short_description(self, instance):
        return instance.description[:25]
    short_description.short_description = _('short description')

    def albums_count(self, instance):
        return instance.albums.count()
    albums_count.short_description = _('album count')

    def episodes_count(self, instance):
        return instance.episodes.count()
    episodes_count.short_description = _('episode count')


class PodcastAlbumAdmin(BaseModelAdmin):
    # prepopulated_fields = {"slug": ("title",)}
    list_display= ('id', 'title', 'frequency', 'keywords', 'explicit', 'status', 'dt_updated',)
    search_fields = ('title', 'hosts__name')
    list_filter = ('status',)
    exclude = ('is_deleted',)
    fieldsets = (
        (None, {
            'fields': (
                'channel',
                'title',
                # 'slug',
                'image',
                'status',
                'hosts',
                'copyright', 'frequency', 'explicit',
                'keywords', 
                'description',
                )
            }),
        )

    def episode_dt_updated(self, obj):
        episode = obj.episodes.latest('dt_created')
        if episode:
            return episode.dt_created
        else:
            return None
    episode_dt_updated.short_description = _('episode updated datetime')


class PodcastEpisodeAdmin(BaseModelAdmin):
    # prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title', 'album__title', 'keywords')
    list_display = ('id', 'title', 'album', 'keywords', 'explicit', 'status', 'dt_updated',)
    list_filter = ('album', 'status')
    fieldsets = (
        (None, {
            'fields': (
                'album',
                'title',
                'subtitle',
                'serial',
                'image',
                'hosts', 
                'preview_file',
                'preview_file_url',
                # 'preview_file_length',
                'full_file',
                'full_file_url',
                # 'full_file_length',
                'copyright',
                'status',
                'explicit',
                'keywords',
                'description',
                )
            }),
        )
#     inlines = (PodcastEnclosureInline,)
#     list_editable = ('status',)
#     raw_id_fields = ('album',)


# class PodcastEnclosureAdmin(BaseModelAdmin):
#     list_display = ('id', 'episode', 'title', 'expression', 'dt_updated')
#     search_fields = ('title', 'episode__title', 'episode__album__title')
#     readonly_fields = ('length', 'size')
#     fields = ('episode', 'title', 'expression', 'file', 'file_url', 'length', 'size')
#     raw_id_fields = ('episode', )




admin.site.register(PodcastChannel, PodcastChannelAdmin)
admin.site.register(PodcastHost, PodcastHostAdmin)
admin.site.register(PodcastAlbum, PodcastAlbumAdmin)
# admin.site.register(PodcastEnclosure, PodcastEnclosureAdmin)
admin.site.register(PodcastEpisode, PodcastEpisodeAdmin)
