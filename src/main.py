from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from src.bot import Bot

app = FastAPI()

app.mount('/static', StaticFiles(directory='src/static'), name='static')

templates = Jinja2Templates(directory='src/templates')


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, 'index.html', {'test': False})


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
