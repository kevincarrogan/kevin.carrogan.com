import os
import pystache
import feedparser
import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()

from pystache.loader import Loader

from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    loader = Loader()
    template = loader.load_name('index')

    lastfm_feed_url = 'http://ws.audioscrobbler.com/1.0/user/kevbear/recenttracks.rss'
    lastfm_feed_result = feedparser.parse(lastfm_feed_url)
    lastfm_entry = lastfm_feed_result.entries[0]
    band, track = lastfm_entry.title.split(u' \u2013 ')
    link = lastfm_entry.link

    ctx = {
        'lastfm_result': {
            'track': track,
            'band': band,
            'link': link,
        }
    }

    return pystache.render(template, ctx)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    http_server = WSGIServer(('0.0.0.0', port), app)
    http_server.serve_forever()
