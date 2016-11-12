from django.contrib import admin
from jet.admin import CompactInline
from django.utils.translation import ugettext_lazy as _

from .utils.admin import BaseModelAdmin
from .models import PodcastHost
from .models import PodcastAlbum
from .models import PodcastEpisode
from .models import PodcastEnclosure


class PodcastEnclosureInline(CompactInline):
    model = PodcastEnclosure
    extra = 0
    readonly_fields = ('is_deleted', 'length', 'size')
    fields = ('title', 
            'expression', 'file',
            'size', 'length',
            )
    show_change_link = True


class PodcastEpisodeInline(CompactInline):
    model = PodcastEpisode
    extra = 0
    readonly_fields = ('is_deleted', )
    fields = ('title', 'slug', 'image', 'copyright', 'status',
            'hosts', 'explicit', 'keywords', 'description',
            )


class PodcastAlbumInline(CompactInline):
    model = PodcastAlbum
    extra = 0


class PodcastHostAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'short_description', 'albums_count', 'episodes_count', 'dt_updated')
    search_fields = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'image', 'description',)
                }),
        )
    ordering = ('name', 'dt_updated')
    readonly_fields = ('is_deleted',)

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
    list_display= ('id', 'title', 'frequency', 'keywords', 'explicit', 'status', 'dt_updated',)
    search_fields = ('title', 'hosts__name')
    readonly_fields = ('is_deleted',)
    fieldsets = (
        (None, {
            'fields': (
                'title', 'slug', 'image',
                'status',
                'hosts',
                'copyright', 'frequency', 'explicit',
                'keywords', 
                'description',
                )
            }),
        )
    inlines = (PodcastEpisodeInline,)

class PodcastEpisodeAdmin(BaseModelAdmin):
    list_display = ('id', 'title', 'album', 'keywords', 'explicit', 'status', 'dt_updated',)
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'image','hosts', 
                'copyright', 'status', 'explicit', 'keywords',
                'description',
                )
            }),
        )
    inlines = (PodcastEnclosureInline,)



class PodcastEnclosureAdmin(BaseModelAdmin):
    list_display = ('id', 'episode', 'title', 'expression', 'dt_updated')
    search_fields = ('title', 'episode__title', 'episode__album__title')
    readonly_fields = ('length', 'size')
    fields = ('episode', 'title', 'expression', 'file', 'length', 'size')
    raw_id_fields = ('episode', )




admin.site.register(PodcastHost, PodcastHostAdmin)
admin.site.register(PodcastAlbum, PodcastAlbumAdmin)
admin.site.register(PodcastEnclosure, PodcastEnclosureAdmin)
admin.site.register(PodcastEpisode, PodcastEpisodeAdmin)
