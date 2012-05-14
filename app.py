import os
import pystache
import feedparser
import json

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
    lastfm_url = 'http://ws.audioscrobbler.com/1.0/user/kevbear/recenttracks.rss'
    lastfm_current_track = feed_entry(lastfm_url)
    lastfm_feed = feedparser.parse(lastfm_url)
    lastfm_recent_tracks = []
    for i in range(5):
        lastfm_recent_tracks.append({
            'title': lastfm_feed.entries[i].title
        })
    lastfm = {
        'title': lastfm_current_track['title'],
        'link': lastfm_current_track['link'],
        'recent_tracks': json.dumps(lastfm_recent_tracks)
    }
    pinboard_url = 'http://feeds.pinboard.in/rss/u:kevindmorgan'
    pinboard_current_bookmark = feed_entry(pinboard_url)
    pinboard_feed = feedparser.parse(pinboard_url)
    pinboard_recent_bookmarks = []
    for i in range(5):
        pinboard_recent_bookmarks.append({
            'title': pinboard_feed.entries[i].title
        })
    pinboard = {
        'title': pinboard_current_bookmark['title'],
        'link': pinboard_current_bookmark['link'],
        'recent_bookmarks': json.dumps(pinboard_recent_bookmarks)
    }
    return pystache.render(
        template,
        {
            'lastfm': lastfm,
            'pinboard': pinboard,
            'instapaper': feed_entry('http://www.instapaper.com/rss/396420/Unm6Hs9KkPouglyWKioGgIHsQ'),
            'twitter': feed_entry('https://twitter.com/statuses/user_timeline/2289741.rss'),
            'github': feed_entry('https://github.com/kevindmorgan.atom'),
        }
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
