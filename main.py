from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
import subprocess
import os
import random

app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/bg", StaticFiles(directory="/usr/share/oichiku/background"), name="background")

templates = Jinja2Templates(directory="templates")


def opdate(date):
    return date[:4] + "/" + date[4:6] + "/" + date[6:8]


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    bgimg = os.listdir("/usr/share/oichiku/background")
    bgimg = bgimg[random.randint(0, len(bgimg) - 1)]
    version = subprocess.check_output(
        ["git", "rev-parse", "--short", "HEAD"], text=True)
    header = templates.get_template('header.html').render({"version": version})
    index_html = templates.get_template('top.html').render({"version": version, "bgimage": bgimg})
    footer = templates.get_template('footer.html').render({"version": version})
    return header + index_html + footer


@app.post("/webhook", response_class=HTMLResponse)
async def webhook():
    res = subprocess.check_output("cd /var/www/oichiku-web; git pull origin master; cd -", text=True, shell=True)
    return res
