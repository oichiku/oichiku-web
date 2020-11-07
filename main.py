from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import subprocess

app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

def test():
    return "Hello World!"

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
  return templates.TemplateResponse("index.html", {"request": request})

@app.post("/webhook")
async def webhook():
    subprocess.call("/home/tomoki/bin/oichiku-deploy")

@app.get("/{path_param}", response_class=HTMLResponse)
async def subdir(path_param, request: Request):
    if path_param == "test":
        return test()
    else:
        return templates.TemplateResponse("404.html", {"request": request})

