import os
import pystache
import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()

from werkzeug.contrib.cache import SimpleCache

from datetime import date

from lastfmclient import LastfmClient

from pystache.loader import Loader

from flask import Flask
app = Flask(__name__)

from letterboxd import get_letterboxd_most_recently_watched_details

cache = SimpleCache()

loader = Loader()

lastfm_key = os.environ.get('lastfm_key')
lastfm_secret = os.environ.get('lastfm_secret')

def milli_seconds_to_duration(milli_seconds):
    total_seconds = milli_seconds / 1000

    minutes = total_seconds / 60
    seconds = total_seconds % 60

    return 'PT{}M{}S'.format(minutes, seconds)


@app.route('/')
def index():
    template = loader.load_name('index')

    lastfm_result = None

    try:
        lastfm_result = cache.get('lastfm_result')
        if not lastfm_result:
            lastfm_client = LastfmClient(lastfm_key, lastfm_secret)
            recent_tracks = lastfm_client.user.get_recent_tracks('kevbear')['track']
            recent_track = recent_tracks[0]
            artist_name = recent_track['artist']['#text']
            track_name = recent_track['name']
            mbid = recent_track['mbid']
            track_info = lastfm_client.track.get_info(
                artist_name,
                track_name,
                mbid,
            )
            lastfm_result = {
                'track': track_info['name'],
                'duration': milli_seconds_to_duration(int(track_info['duration'])),
                'album': track_info['album']['title'],
                'artist': track_info['artist']['name'],
                'url': track_info['url'],
            }
            cache.set('lastfm_result', lastfm_result, timeout=120)
    except:
        pass

    ctx = {
        'lastfm_result': lastfm_result,
        'letterboxd_result': get_letterboxd_most_recently_watched_details(),
        'year': date.today().year,
    }

    return pystache.render(template, ctx)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    http_server = WSGIServer(('0.0.0.0', port), app)
    http_server.serve_forever()
