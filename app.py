from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import joblib

app = FastAPI()
popular_df = joblib.load('popular.joblib')

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html",
    {"request": request,
     "book_name" : list(popular_df['Book-Title'].values),
     "author" : list(popular_df['Book-Author'].values),
     "images" : list(popular_df['Image-URL-M'].values),
     "votes" : list(popular_df['num_ratings'].values),
     "ratings" : list(popular_df['avg_rating'].values),
    })


@app.get("/recommend", response_class=HTMLResponse)
async def recommend(request: Request):
    return templates.TemplateResponse("recommend.html", {"request": request})