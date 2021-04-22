import os
import secrets
from subprocess import run, PIPE
from urllib.parse import urlparse

from fastapi import FastAPI, Request, Cookie, Form, HTTPException, Depends
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
from hashlib import sha256
import mydb

templates = Jinja2Templates(directory="templates")

app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")


class RequiresLoginException(Exception):
    pass


async def auth(sessid: Optional[str] = Cookie(None)):
    if sessid:
        db = mydb.get_session(sessid)
        if db:
            return db.user_id
    raise RequiresLoginException


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


@app.exception_handler(RequiresLoginException)
async def exception_handler(request: Request, exc: RequiresLoginException):
    return RedirectResponse(url="/login?redirect=" + str(request.url))


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


@app.get("/login", response_class=HTMLResponse)
async def loginpage(redirect: Optional[str] = None):
    html = templates.get_template("login.html").render({"redirect": redirect})
    return html


@app.post("/login")
async def login(
    user_id: str = Form(...),
    password: str = Form(...),
    redirect: Optional[str] = Form(None),
):
    db = mydb.get_user(user_id)
    if not db or sha256(password.encode()).hexdigest() != db.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    sessid = secrets.token_hex(32)
    mydb.set_session(sessid, user_id)
    res = RedirectResponse(redirect, status_code=302)
    res.set_cookie(key="sessid", value=sessid)
    return res


@app.get("/logout")
async def logout(sessid: Optional[str] = Cookie(None)):
    if sessid:
        db = mydb.get_session(sessid)
        if db:
            mydb.del_session(sessid)
            return RedirectResponse("/", status_code=302)
    return HTMLResponse(
        content=templates.get_template("404.html").render({}),
        status_code=404,
    )


@app.get("/private")
async def private(user_id: str = Depends(auth)):
    return {"hello": user_id}
