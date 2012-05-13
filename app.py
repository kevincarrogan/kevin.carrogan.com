import os
import pystache
import feedparser

from pystache.loader import Loader

from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    lastfm_feed = feedparser.parse('http://ws.audioscrobbler.com/1.0/user/kevbear/recenttracks.rss')
    loader = Loader()
    template = loader.load_name('index')
    return pystache.render(
        template,
        {
            'lastfm': lastfm_feed.entries[0]
        }
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
