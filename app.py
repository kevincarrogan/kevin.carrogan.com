import os
import pystache
import feedparser
import json
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
    feeds = {
        'lastfm': 'http://ws.audioscrobbler.com/1.0/user/kevbear/recenttracks.rss',
        'pinboard': 'http://feeds.pinboard.in/rss/u:kevindmorgan',
        'instapaper': 'http://www.instapaper.com/rss/396420/Unm6Hs9KkPouglyWKioGgIHsQ',
        'github': 'https://github.com/kevincarrogan.atom',
    }
    feed_results = {}
    jobs = [gevent.spawn(feedparser.parse, url) for url in feeds.values()]
    gevent.joinall(jobs)

    for name, feed in zip(feeds.keys(), jobs):
        current = feed.value.entries[0]
        feed_results[name] = {
            'title': current.title,
            'link': current.link,
            'items': json.dumps([item.title for item in feed.value.entries[:5]])
        }

    return pystache.render(
        template,
        feed_results
    )


@app.route('/personal/')
def personal():
    loader = Loader()
    template = loader.load_name('personal')
    return pystache.render(
        template,
        {}
    )


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    http_server = WSGIServer(('0.0.0.0', port), app)
    http_server.serve_forever()
