import io

import numpy as np
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from matplotlib import pyplot as plt
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse

from schemas import TransformRequest
from services.convert_vba import utm_to_latlon, convert_coordinates
from services.geo import raw_decode, geo_decode_gpx, google_decode
from services.plt_pic import get_plot

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/geocode_list")
async def geocode_list(request: Request):
    d = await request.json()
    x = raw_decode(d["address"], screen=True)
    return x


@app.post("/api/geocode_gpx")
async def geocode_gpx(request: Request):
    d = await request.json()
    x = raw_decode(d["address"])
    return geo_decode_gpx(x)


@app.post("/api/google_list")
async def google_list(request: Request):
    d = await request.json()
    x = google_decode(d["address"], screen=True)
    return x


@app.post("/api/google_gpx")
async def google_gpx(request: Request):
    d = await request.json()
    x = google_decode(d["address"])
    return geo_decode_gpx(x)


@app.post("/transform")
async def transform_value(request: TransformRequest):
    transformed_value = utm_to_latlon(request.value)
    transformed_value = convert_coordinates(transformed_value)

    return {"original": request.value, "transformed": transformed_value}


@app.get("/api/plot")
async def plot():
    # Пример данных
    coordinates = [(1, 2), (2, 3), (3, 5), (4, 7), (5, 11)]

    # Разделяем на X и Y
    x, y = zip(*coordinates)
    x, y = np.array(x), np.array(y)

    # Создаем график
    plt.figure()
    plt.plot(x, y, marker='o')
    plt.title('Линия по координатам')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)

    # Сохраняем график в буфер
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)  # Перемещаем курсор в начало файла

    # Возвращаем изображение как ответ
    return StreamingResponse(img, media_type="image/png")


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5555)
