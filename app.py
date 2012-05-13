import os
import pystache
import feedparser

from pystache.loader import Loader

from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    def feed_entry(url):
        feed = feedparser.parse(url)
        return feed.entries[0]
    loader = Loader()
    template = loader.load_name('index')
    return pystache.render(
        template,
        {
            'lastfm': feed_entry('http://ws.audioscrobbler.com/1.0/user/kevbear/recenttracks.rss'),
            'pinboard': feed_entry('http://feeds.pinboard.in/rss/u:kevindmorgan'),
            'instapaper': feed_entry('http://www.instapaper.com/rss/396420/Unm6Hs9KkPouglyWKioGgIHsQ'),
            'twitter': feed_entry('https://twitter.com/statuses/user_timeline/2289741.rss')
        }
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
