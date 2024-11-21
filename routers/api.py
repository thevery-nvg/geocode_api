from fastapi import Request, APIRouter
from schemas import TransformRequest
from services.convert_vba import conv_coordinates_full
from services.geo import raw_decode, geo_decode_gpx, google_decode

from services.tomsk_autocad import autocad_decode_api
from services.megion import parse_pipeline
api_router = APIRouter(
    prefix="/api"
)


@api_router.post("/geocode_list")
async def geocode_list(request: Request):
    d = await request.json()
    x = raw_decode(d["address"], screen=True)
    return x


@api_router.post("/geocode_gpx")
async def geocode_gpx(request: Request):
    d = await request.json()
    x = raw_decode(d["address"])
    return geo_decode_gpx(x)


@api_router.post("/google_list")
async def google_list(request: Request):
    d = await request.json()
    x = google_decode(d["address"], screen=True)
    return x


@api_router.post("/google_gpx")
async def google_gpx(request: Request):
    d = await request.json()
    x = google_decode(d["address"])
    return geo_decode_gpx(x)


@api_router.post("/transform")
async def transform_value(request: TransformRequest):
    transformed_value = conv_coordinates_full(request.value)
    return {"original": request.value, "transformed": transformed_value}


@api_router.post("/draw_tomsk")
async def try_parse_vba_json(request: Request):
    data = await request.json()
    print("Received JSON:", data)
    a = autocad_decode_api(data)
    return a


@api_router.post("/megion")
async def try_parse_vba_json1(request: Request):
    data = await request.json()
    a = parse_pipeline(data)
    for k in a:
        print(f"{k=} {a[k]=}")
    return a