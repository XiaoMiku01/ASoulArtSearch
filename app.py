import fastapi
from starlette.responses import JSONResponse
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from fastapi import File, UploadFile
import cv2
import numpy as np
from utils import *
app = fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/demo")
async def get_index(request: Request):
    return templates.TemplateResponse("demo.html", {"request": request})


@app.post("/api/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    if file.content_type not in ("image/jpeg", "image/png", "image/jpg", "image/webp"):
        responses = {
            "code": -1,
            "message": "不支持你上传的图片格式"
        }
        return JSONResponse(responses)
    image = cv2.imdecode(np.frombuffer(await file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    hash1 = await pHash(image)
    all_data = await read_json('./data/data.json')
    img_list = []
    for data in all_data:
        if data['pHash'] in (None, '0x0'):
            continue
        hanming = Hamming_distance(hash1, data['pHash'])
        if hanming <= 5:
            img_list.append({'detail': data, 'similarity': round((18-hanming)/18, 4)})
    img_list.sort(key=lambda x: x['similarity'], reverse=True)
    if len(img_list) == 0:
        responses = {
            "code": -1,
            "message": "没有相似的图片",
            "last_time": all_data[0]['load_time'],
        }
        return JSONResponse(responses)
    responses = {
        "code": 0,
        "message": "查询成功",
        "data": img_list[:3],
        "last_time": all_data[0]['load_time'],
    }
    return JSONResponse(responses)
if __name__ == "__main__":
    uvicorn.run(app='app:app', host="127.0.0.1", port=1211, reload=True)
