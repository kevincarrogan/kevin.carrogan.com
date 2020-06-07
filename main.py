import asyncio
import math

from aiocache import Cache

from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from letterboxd import get_letterboxd_most_recently_watched_details
from work import get_current_work_place

templates = Jinja2Templates(directory="templates")

cache = Cache(Cache.MEMORY)


async def cache_letterboxd_result():
    letterboxd_result = await get_letterboxd_most_recently_watched_details()
    await cache.set("letterboxd_result", letterboxd_result, math.inf)
    return letterboxd_result


async def index(request):
    letterboxd_result = await cache.get("letterboxd_result")
    asyncio.create_task(cache_letterboxd_result())

    work_result = get_current_work_place()

    ctx = {
        "letterboxd_result": letterboxd_result,
        "work_result": work_result,
        "request": request,
    }
    return templates.TemplateResponse("index.html", ctx)


routes = [Route("/", index), Mount("/static", StaticFiles(directory="static"))]


async def fill_cache():
    await cache_letterboxd_result()


app = Starlette(routes=routes, on_startup=[fill_cache])
