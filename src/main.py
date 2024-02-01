from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount('/static', StaticFiles(directory='src/static'), name='static')


@app.get('/')
async def index():
    return FileResponse('src/static/index.html')


@app.post('/predict')
async def predict(request: Request):
    body = await request.body()
    board_str = body.decode('utf-8')
    return {'move': 1}
