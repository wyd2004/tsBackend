from django.utils.translation import ugettext_lazy as _
from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard, AppIndexDashboard


class CustomIndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        self.children.append(modules.RecentActions( 
            _('Recent Actions'),
            10, 
            column=2,
            order=1
        ))

        self.children.append(modules.AppList(
            _('podcast data'),
            models = [
                'podcast.PodcastHost',
                'podcast.PodcastAlbum',
                'podcast.PodcastEpisode',
                'podcast.PodcastEnclosure',
                ],
            column=0,
            order=2
        ))

        self.children.append(modules.AppList(
            _('member data'),
            models = [
                'member.Member',
                'member.PodcastAlbumSubscription',
                ],
            column=1,
            order=0
        ))
