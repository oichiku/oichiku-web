import os
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
from jinja2 import Template
from starlette.exceptions import HTTPException as StarletteHTTPException
import mydb

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
    title, content, created_at, updated_at = mydb.get_post(0)
    header = templates.get_template("header.html").render(
        {"title": title, "version": updated_at}
    )
    print(content)
    contentHTML = Template(content).render({"version": updated_at})
    footer = templates.get_template("footer.html").render({"version": updated_at})
    return header + contentHTML + footer
