import os
import pystache
import feedparser
import json

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

    for name, url in feeds.iteritems():
        feed = feedparser.parse(url)
        current = feed.entries[0]
        feed_results[name] = {
            'title': current.title,
            'link': current.link,
            'items': json.dumps([item.title for item in feed.entries[:5]])
        }

    return pystache.render(
        template,
        feed_results
    )


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
