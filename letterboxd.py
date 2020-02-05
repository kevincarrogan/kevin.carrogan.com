import httpx
import random

from xml.etree import ElementTree


LETTERBOXD_RSS_URL = "https://letterboxd.com/kevincarrogan/rss/"


def get_review_from_rating(rating):
    ratings_to_review_map = {
        "5.0": ["pretty much perfect", "one of the best films I've ever seen"],
        "4.5": ["almost perfect", "a must watch"],
        "4.0": ["pretty great"],
        "3.5": ["better than most"],
        "3.0": ["slightly better than average"],
        "2.5": ["completely average", "mediocre"],
        "2.0": ["passable", "mediocre at best"],
        "1.5": ["slightly redeemable, but not much"],
        "1.0": ["not worth watching again"],
        "0.5": [
            "absolutely dire",
            "one of the worst films I've ever seen",
            "anger inducing",
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


async def get_letterboxd_most_recently_watched_details():
    async with httpx.AsyncClient() as client:
        letterboxd_response = await client.get(LETTERBOXD_RSS_URL)

    film_title, film_rating, film_url = get_film_details_from_response(
        letterboxd_response
    )
    film_review = get_review_from_rating(film_rating)

    return {"title": film_title, "review": film_review, "url": film_url}
