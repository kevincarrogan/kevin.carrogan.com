import random
import requests

from xml.etree import ElementTree


LETTERBOXD_RSS_URL = "https://letterboxd.com/kevincarrogan/rss/"


def get_review_from_rating(rating):
    ratings_to_review_map = {
        "5.0": [
            "pretty much perfect",
            "one of the best films I've ever seen",
            "I'm not quite sure why I'm not watching this right now",
        ],
        "4.5": ["almost perfect", "a must watch"],
        "4.0": ["pretty great"],
        "3.5": ["better than most"],
        "3.0": ["slightly better than average"],
        "2.5": ["completely average", "mediocre"],
        "2.0": ["passable", "mediocre at best"],
        "1.5": ["some very slight reedemable qualities"],
        "1.0": [
            "not worth watching again",
            "I'd be pretty sad to have to watch this again",
        ],
        "0.5": [
            "absolutely dire",
            "will never watch again",
            "one of the worst films I've ever seen",
            "legitimately makes me angry",
        ],
    }

    possible_reviews = ratings_to_review_map[rating]
    review = random.choice(possible_reviews)

    return review


def get_film_details_from_response(response):
    root = ElementTree.fromstring(response.content)
    channel = root.find("channel")
    items = channel.findall("item")
    latest_item = items[0]
    film_title = latest_item.find("{https://letterboxd.com}filmTitle").text
    film_rating = latest_item.find("{https://letterboxd.com}memberRating").text
    film_url = latest_item.find("link").text

    return film_title, film_rating, film_url


def get_letterboxd_most_recently_watched_details():
    letterboxd_response = requests.get(LETTERBOXD_RSS_URL)

    film_title, film_rating, film_url = get_film_details_from_response(
        letterboxd_response
    )
    film_review = get_review_from_rating(film_rating)

    return {"title": film_title, "review": film_review, "url": film_url}
