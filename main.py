from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from services.geo import Coordinates, CreateGPX

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


@app.post("/api/geocode")
async def test_geocode(request: Request):
    d = await request.json()
    crd = Coordinates(d.get("address"))
    wrt = CreateGPX()
    x=wrt(crd())
    return {"result": x}


@app.post("/api/geocode_gpx")
async def test_geocode(request: Request):
    d = await request.json()
    return {"result": "Geocoded successfully"}


if __name__ == '__main__':
    uvicorn.run(app)
