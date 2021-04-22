import os
import secrets
from subprocess import run, PIPE
from urllib.parse import urlparse

from fastapi import FastAPI, Request, Cookie, Form, HTTPException
from fastapi.responses import (
    HTMLResponse,
    PlainTextResponse,
    RedirectResponse,
    Response,
)
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import Template
from typing import Optional
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
        domain = os.getenv("DOMAIN")
        if domain:
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
    author, title, content, created_at, updated_at = mydb.get_post(0)
    gitver = run(
        "git rev-parse --short HEAD", shell=True, stdout=PIPE, text=True
    ).stdout
    version = gitver + "-" + str(updated_at)
    header = templates.get_template("header.html").render(
        {"title": title, "version": version}
    )
    contentHTML = Template(content).render({"version": updated_at})
    footer = templates.get_template("footer.html").render({"version": version})
    return header + contentHTML + footer


@app.get("/admin", response_class=HTMLResponse)
async def adminpage(sessid: Optional[str] = Cookie(None)):
    if sessid:
        db = mydb.get_session(sessid)
        if db:
            return db.user_id
    res = '<form method="POST">\
        <input name="user_id">\
        <input name="password" type="password">\
        <input type="submit">\
        </form>'
    return res


@app.post("/admin")
async def login(user_id: str = Form(...), password: str = Form(...)):
    db = mydb.get_user(user_id)
    if not db or password != db.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    sessid = secrets.token_hex(32)
    mydb.set_session(sessid, user_id)
    res = RedirectResponse("/admin", status_code=302)
    res.set_cookie(key="sessid", value=sessid)
    return res
