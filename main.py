from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
import subprocess
import os
import random


templates = Jinja2Templates(directory="templates")

async def not_found(request, exc):
    return templates.get_template('404.html')

exceptions = {
    404: not_found,
}

app = FastAPI(docs_url=None, redoc_url=None, exception_handlers=exceptions)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/bg", StaticFiles(directory="/usr/share/oichiku/background"), name="background")


def opdate(date):
    return date[:4] + "/" + date[4:6] + "/" + date[6:8]


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    bgimg = os.listdir("/usr/share/oichiku/background")
    bgimg = bgimg[random.randint(0, len(bgimg) - 1)]
    version = subprocess.check_output(
        ["git", "rev-parse", "--short", "HEAD"], text=True)
    header = templates.get_template('header.html').render({"version": version})
    index_html = templates.get_template('top.html').render({"version": version, "bgimg": bgimg})
    footer = templates.get_template('footer.html').render({"version": version})
    return header + index_html + footer


@app.post("/webhook", response_class=HTMLResponse)
async def webhook():
    res = subprocess.run("/usr/share/oichiku/bin/update")
    return res
