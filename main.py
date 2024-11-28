import os
from http.client import HTTPException
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

from routers.api import api_router

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
app.include_router(api_router)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/snake", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("snake.html", {"request": request})

FILES_DIR = Path("C:\\Users\\box7\\Downloads")


@app.get("/files", response_class=HTMLResponse)
async def send_files(request: Request):
    files = os.listdir(FILES_DIR)
    return templates.TemplateResponse("files.html", {"request": request, "files": files})


@app.get("/files/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(FILES_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, filename=filename)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5555)
