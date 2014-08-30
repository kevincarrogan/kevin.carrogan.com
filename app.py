import os
import pystache
import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()

from lastfmclient import LastfmClient

from pystache.loader import Loader

from flask import Flask
app = Flask(__name__)

lastfm_key = os.environ.get('lastfm_key')
lastfm_secret = os.environ.get('lastfm_secret')

@app.route('/')
def index():
    loader = Loader()
    template = loader.load_name('index')

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

    ctx = {
        'lastfm_result': {
            'track': track_info['name'],
            'duration': track_info['duration'],
            'album': track_info['album']['title'],
            'artist': track_info['artist']['name'],
            'url': track_info['url'],
        }
    }

    return pystache.render(template, ctx)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    http_server = WSGIServer(('0.0.0.0', port), app)
    http_server.serve_forever()
