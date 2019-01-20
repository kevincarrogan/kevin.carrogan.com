import requests

from xml.etree import ElementTree


LETTERBOXD_RSS_URL = 'https://letterboxd.com/kevincarrogan/rss/'


def get_letterboxd_most_recently_watched_details():
    letterboxd_response = requests.get(LETTERBOXD_RSS_URL)

    tree = ElementTree.fromstring(letterboxd_response.content)
    channel = tree.find('channel')
    items = channel.findall('item')
    latest_item = items[0]
    film_title = latest_item.find('{https://letterboxd.com}filmTitle').text
    film_rating = latest_item.find('{https://letterboxd.com}memberRating').text
    film_review = 'a {} out of 5 star film'.format(film_rating)

    return {
        'title': film_title,
        'review': film_review,
    }
