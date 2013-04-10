import os
import pystache
import feedparser
import json
import gevent
import gevent.monkey
import requests
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
        'twitter': 'http://api.twitter.com/1/statuses/user_timeline.rss?screen_name=kevindmorgan',
        'instapaper': 'http://www.instapaper.com/rss/396420/Unm6Hs9KkPouglyWKioGgIHsQ',
        'github': 'https://github.com/kevindmorgan.atom',
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


@app.route('/status-board/lastfm/')
def lastfm():
    loader = Loader()
    template = loader.load_name('lastfm')

    content = requests.get('http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=kevbear&api_key=%s&format=json&limit=1' % os.environ.get('lastfm_key', '')).content
    track_info = json.loads(content)['recenttracks']['track'][0]
    lastfm_results = {
        'artist': track_info['artist']['#text'],
        'track': track_info['name'],
        'image_url': track_info['image'][0]['#text'],
    }

    return pystache.render(
        template,
        lastfm_results,
    )


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    http_server = WSGIServer(('0.0.0.0', port), app)
    http_server.serve_forever()
