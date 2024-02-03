from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.bot import Bot


class Predict(BaseModel):
    board: str
    test: bool


app = FastAPI()

app.mount('/static', StaticFiles(directory='src/static'), name='static')


@app.get('/')
async def index():
    return FileResponse('src/static/index.html')

@app.get('/test')
async def test_index():
    return FileResponse('src/static/test.index.html')

@app.post('/predict')
async def predict(predict: Predict):
    if predict.test:
        bot = Bot(strategy='fixed')
    else:
        bot = Bot(strategy='random')
    prediction = bot.predict(predict.board)
    return {'move': prediction}
