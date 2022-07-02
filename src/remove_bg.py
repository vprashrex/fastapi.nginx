import base64
import logging
from fastapi import FastAPI, File, Request, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import utils
import numpy as np
from imageio import imread
import io

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("pic-ai.html", context={"request": request})

@app.get("/augmentation", response_class=HTMLResponse)
async def augmentation(request: Request):
    return templates.TemplateResponse("augmentation.html", context={"request": request})

@app.post("/", response_class=HTMLResponse)
async def remove_bg(request: Request, file:dict):
    try:
        file = file['img']
        content = file.split(';')[1]
        img_encoded = content.split(',')[1]
        img = imread(io.BytesIO(base64.b64decode(img_encoded)))
        if img.shape[2] == 4:
            img = img[:,:,0:3]
        img_pil = utils.bg_remove(img)
        output_image = utils.encode_array_to_base64(img_pil)
        
        return JSONResponse(
            status_code=200,
            content={
                'img_with_bk': output_image
            },
        )
    except Exception as ex:
        logging.info(ex)
        print(ex)
        return JSONResponse(status_code=400, content={"error": str(ex)})

if __name__ == '__main__':
    uvicorn.run(app,port=5050)