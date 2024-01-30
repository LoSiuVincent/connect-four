from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")


@app.get("/")
async def index():
    return FileResponse("src/static/index.html")
