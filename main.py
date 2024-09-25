from io import BytesIO

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
from services.autocad import autocad_decode

plot_list = []
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


@app.get("/api/autocad")
async def autocad():
    autocad_decode()


@app.post("/transform")
async def transform_value(request: TransformRequest):
    transformed_value = utm_to_latlon(request.value)
    transformed_value = convert_coordinates(transformed_value)

    return {"original": request.value, "transformed": transformed_value}


@app.get("/api/plot")
async def plot():
    s = [
        (60.96212, 70.87592),
        (60.96212, 70.87600),
        (60.96207, 70.87632),
        (60.96203, 70.87643),
        (60.96190, 70.87728),
        (60.96170, 70.87860),
        (60.96150, 70.87993),
        (60.96130, 70.88122),
        (60.96110, 70.88250),
        (60.96052, 70.88268),

    ]
    # Пример данных
    coordinates = np.array(s)

    # Нормализация данных
    def normalize(data):
        min_vals = np.min(data, axis=0)
        max_vals = np.max(data, axis=0)
        return (data - min_vals) / (max_vals - min_vals)

    normalized_coordinates = normalize(coordinates)

    # Разделяем на X и Y после нормализации
    x, y = normalized_coordinates[:, 0], normalized_coordinates[:, 1]

    # Создаем график
    plt.figure()
    plt.plot(x, y, marker='o')
    plt.title('Нормализованная линия по координатам')
    plt.xlabel('Normalized X')
    plt.ylabel('Normalized Y')
    plt.grid(True)

    # Настройка осей для отображения нормализованного диапазона
    plt.xlim(-1.5, 1.5)
    plt.ylim(-1.5, 1.5)

    # Сохраняем график в буфер
    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)  # Перемещаем курсор в начало файла

    # Возвращаем изображение как ответ
    return StreamingResponse(img, media_type="image/png")


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5555)
