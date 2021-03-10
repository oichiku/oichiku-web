from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
# import pandas as pd
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
    index_html = templates.get_template('index.html').render({"version": version, "bgimage": bgimg})
    footer = templates.get_template('footer.html').render({"version": version})
    return header + index_html + footer


@app.get("/article", response_class=HTMLResponse)
async def article(request: Request):
    bgimg = os.listdir("/usr/share/oichiku/background")
    bgimg = bgimg[random.randint(0, len(bgimg) - 1)]
    version = subprocess.check_output(
        ["git", "rev-parse", "--short", "HEAD"], text=True)
    return templates.TemplateResponse("article.html", {"request": request, "bgimage": bgimg, "version": version})


@app.get("/article/view", response_class=HTMLResponse)
async def article_view(request: Request, id: Optional[str] = None):
    csv = pd.read_csv("/usr/share/list.csv", encoding="utf_8", dtype=object)
    csv = csv[csv.isenable == "1"]
    if (csv.id == id).sum() == 0:
        return templates.TemplateResponse("404.html", {"request": request})
    bgimg = os.listdir("/usr/share/oichiku/background")
    bgimg = bgimg[random.randint(0, len(bgimg) - 1)]
    version = subprocess.check_output(
        ["git", "rev-parse", "--short", "HEAD"], text=True)
    with open("/usr/share/oichiku/html/" + id + ".html", "r") as f:
        content = f.read()
    content = "<style>noarticle{display:none;}server{display:inline;}</style>\n" + content
    title = csv.title[csv.id == id].iloc[-1]
    created = csv.created[csv.id == id].iloc[-1]
    created = opdate(created)
    return templates.TemplateResponse("article-view.html", {"request": request, "bgimage": bgimg, "version": version, "title": title, "created": created, "content": content})


@app.post("/webhook", response_class=HTMLResponse)
async def webhook():
    res = subprocess.check_output("cd /var/www/oichiku-web; git pull origin master; cd -", text=True)
    return res
