from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from schemas import TransformRequest
from services.convert_vba import conv_coordinates_full
from services.geo import raw_decode, geo_decode_gpx, google_decode
import json
from services.tomsk_autocad import autocad_decode_api

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


@app.post("/transform")
async def transform_value(request: TransformRequest):
    transformed_value = conv_coordinates_full(request.value)
    return {"original": request.value, "transformed": transformed_value}


@app.post("/json_ttt")
async def try_parse_vba_json(request: Request):
    data = await request.json()
    print("Received JSON:", data)
    a = autocad_decode_api(data)
    output = json.dumps(a)
    # возможно стоит возвращать  output,потом будет видно работает или нет.
    # Но вроде работало
    return a


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5555)
