from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from schemas import TransformRequest
from services.convert_vba import utm_to_latlon, convert_coordinates
from services.geo import geo_coding, geo_coding_full, google_decode_full, google_decode

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
async def test_geocode(request: Request):
    d = await request.json()
    x = geo_coding(d["address"])
    return x


@app.post("/api/geocode_gpx")
async def test_geocode(request: Request):
    d = await request.json()
    x = geo_coding_full(d["address"])
    return x


@app.post("/api/google_list")
async def test_geocode(request: Request):
    d = await request.json()
    x = google_decode(d["address"])
    return x


@app.post("/api/google_gpx")
async def test_geocode(request: Request):
    d = await request.json()
    x = google_decode_full(d["address"])
    return x


@app.post("/transform")
async def transform_value(request: TransformRequest):
    transformed_value = utm_to_latlon(request.value)
    transformed_value = convert_coordinates(transformed_value)

    return {"original": request.value, "transformed": transformed_value}


if __name__ == '__main__':
    uvicorn.run(app)
