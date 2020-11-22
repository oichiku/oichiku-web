from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import subprocess, os, random

app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/bg", StaticFiles(directory="../admin/background"), name="background")

templates = Jinja2Templates(directory="templates")

def test():
    return "Hello World!"

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    bgimg = os.listdir("../admin/background")
    bgimg = bgimg[random.randint(0,len(bgimg)-1)]
    version = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True)
    return templates.TemplateResponse("index.html", {"request": request, "bgimage": bgimg, "version": version})

@app.post("/webhook", response_class=HTMLResponse)
async def webhook():
    res = subprocess.check_output("/root/bin/oichiku-deploy", text=True)
    return res

@app.get("/{path_param}", response_class=HTMLResponse)
async def subdir(path_param, request: Request):
    if path_param == "test":
        return test()
    else:
        return templates.TemplateResponse("404.html", {"request": request})

