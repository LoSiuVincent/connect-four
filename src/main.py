from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from src.bot import Bot

app = FastAPI()

app.mount('/static', StaticFiles(directory='src/static'), name='static')

templates = Jinja2Templates(directory='src/templates')


@app.get('/')
async def index():
    return FileResponse('src/static/index.html')


@app.get('/test', response_class=HTMLResponse)
async def test_index(request: Request):
    return templates.TemplateResponse(request, 'index.html', {'test': True})


class Predict(BaseModel):
    board: str
    test: bool


@app.post('/predict')
async def predict(predict: Predict):
    if predict.test:
        bot = Bot(strategy='fixed')
    else:
        bot = Bot(strategy='random')
    prediction = bot.predict(predict.board)
    return {'move': prediction}
