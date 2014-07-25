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

    feeds = {
        'lastfm': 'http://ws.audioscrobbler.com/1.0/user/kevbear/recenttracks.rss',
    }

    feed_results = {}
    jobs = [gevent.spawn(feedparser.parse, url) for url in feeds.values()]
    gevent.joinall(jobs)

    for name, feed in zip(feeds.keys(), jobs):
        current = feed.value.entries[0]
        feed_results[name] = {
            'title': current.title,
            'link': current.link,
        }

    return pystache.render(template, feed_results)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    http_server = WSGIServer(('0.0.0.0', port), app)
    http_server.serve_forever()
