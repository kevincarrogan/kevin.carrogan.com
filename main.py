import asyncio

from aiocache import Cache

from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from letterboxd import get_letterboxd_most_recently_watched_details

templates = Jinja2Templates(directory="templates")

cache = Cache(Cache.MEMORY)


async def cache_letterboxd_result():
    letterboxd_result = await get_letterboxd_most_recently_watched_details()
    await cache.set("letterboxd_result", letterboxd_result, 60 * 60)
    return letterboxd_result


async def index(request):
    letterboxd_result = await cache.get("letterboxd_result")
    asyncio.create_task(cache_letterboxd_result())

    ctx = {"letterboxd_result": letterboxd_result, "request": request}
    return templates.TemplateResponse("index.html", ctx)


routes = [Route("/", index), Mount("/static", StaticFiles(directory="static"))]

app = Starlette(routes=routes)
