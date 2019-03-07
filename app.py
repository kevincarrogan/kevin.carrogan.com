import os
import pystache
import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()

from werkzeug.contrib.cache import SimpleCache

from datetime import date

from pystache.loader import Loader

from flask import Flask
from flask_compress import Compress
from flask_talisman import Talisman, GOOGLE_CSP_POLICY
app = Flask(__name__)
Compress(app)
Talisman(app, content_security_policy=GOOGLE_CSP_POLICY)

from letterboxd import get_letterboxd_most_recently_watched_details

cache = SimpleCache()

loader = Loader()


def get_cached_result(func, key):
    cached_result = None

    try:
        cached_result = cache.get(key)
        if not cached_result:
            cached_result = func()
            cache.set(key, cached_result)
    except:
        pass

    return cached_result


@app.route('/')
def index():
    template = loader.load_name('index')

    letterboxd_result = get_cached_result(
        get_letterboxd_most_recently_watched_details,
        'letterboxd_result',
    )

    ctx = {
        'letterboxd_result': letterboxd_result,
    }

    return pystache.render(template, ctx)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    http_server = WSGIServer(('0.0.0.0', port), app)
    http_server.serve_forever()
