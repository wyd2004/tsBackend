import re
import requests

from podcast.models import PodcastEpisode
from podcast.models import PodcastEnclosure

url_map = {
        1: 'http://music.weibo.com/snake/boke_boke.php?bid=6858',
        2: 'http://music.weibo.com/snake/boke_boke.php?bid=28870',
        3: 'http://music.weibo.com/snake/boke_boke.php?bid=6876',
        4: 'http://music.weibo.com/snake/boke_boke.php?bid=6892',
        5: 'http://music.weibo.com/snake/boke_boke.php?bid=6874',
        6: 'http://music.weibo.com/snake/boke_boke.php?bid=6894',
        7: 'http://music.weibo.com/snake/boke_boke.php?bid=6904',
        8: 'http://music.weibo.com/snake/boke_boke.php?bid=59394',
        9: 'http://music.weibo.com/snake/boke_boke.php?bid=6866',
        10: 'http://music.weibo.com/snake/boke_boke.php?bid=154554',
        }

def parse_album_page(url):
    rex = re.compile(r'<span class="songname.*?html">(.*)</a>')
    res = requests.get(url)
    if res.ok:
        episodes = rex.findall(res.content)
        episodes.reverse()
        return episodes
    else:
        return []

def fetch_eipsode():
    for album_id, url in url_map.items():
        episodes = parse_album_page(url)
        for title in episodes:
            title = title.strip()
            episode, create = PodcastEpisode.objects.get_or_create(
                    album_id=album_id,
                    title=title,
                    )

def generate_enclosure():
    for episode in PodcastEpisode.objects.all():
        enclosure, create = PodcastEnclosure.objects.get_or_create(
                episode=episode,
                title='%s - preview' % episode.title,
                file_url='http://preview.mp3',
                expression='preview',
                length=5 * 60,
                )
        enclosure, create = PodcastEnclosure.objects.get_or_create(
                episode=episode,
                title='%s - full' % episode.title,
                file_url='http://full.mp3',
                expression='full',
                length=30 * 60,
                )
