from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html",context={"request":request})

