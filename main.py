import os
import subprocess
from urllib.parse import urlparse

from fastapi import FastAPI, Request
from fastapi.responses import (
    HTMLResponse,
    PlainTextResponse,
    RedirectResponse,
    Response,
)
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

templates = Jinja2Templates(directory="templates")

app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    if request.method == "HEAD":
        return Response()
    elif "herokuapp" in urlparse(str(request.url)).netloc:
        domain = os.getenv("DOMAIN", "example.com")
        url = urlparse(str(request.url))._replace(netloc=domain).geturl()
        response = RedirectResponse(url)
    else:
        response = await call_next(request)
    return response


@app.exception_handler(StarletteHTTPException)
async def my_exception_handler(request, exception):
    if exception.status_code == 404:
        return HTMLResponse(
            content=templates.get_template("404.html").render({}),
            status_code=exception.status_code,
        )
    else:
        return PlainTextResponse(
            str(exception.detail), status_code=exception.status_code
        )


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    version = subprocess.run("git rev-parse --short HEAD", shell=True)
    header = templates.get_template("header.html").render({"version": version})
    index_html = templates.get_template("top.html").render({"version": version})
    footer = templates.get_template("footer.html").render({"version": version})
    return header + index_html + footer
