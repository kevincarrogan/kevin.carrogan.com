from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from sites import SITES
from work import get_current_work_place

templates = Jinja2Templates(directory="templates")


async def index(request):
    work_result = get_current_work_place()

    ctx = {
        "sites": SITES,
        "work_result": work_result,
        "request": request,
    }
    return templates.TemplateResponse("index.html", ctx)


routes = [Route("/", index), Mount("/static", StaticFiles(directory="/app/static"))]


app = Starlette(routes=routes)
