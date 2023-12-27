from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import joblib
from fastapi import FastAPI, Form
from typing import Annotated
import numpy as np

app = FastAPI()
popular_df = joblib.load('popular.joblib')
pt = joblib.load('pt.joblib')
books = joblib.load('books.joblib')
similarity_scores = joblib.load('similarity_scores.joblib')

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
async def recommend_ui(request: Request):
    return templates.TemplateResponse("recommend.html", {"request": request})

@app.post("/recommend_books")
async def recommend(request:Request):
    form = await request.form()
    formDict = dict(form)
    user_input = formDict["user_input"]
    # index fetch
    index = np.where(pt.index==user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x:x[1], reverse=True)[1:6]
    
    data = []
    # looping items
    for i in similar_items:
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item = temp_df.drop_duplicates('Book-Title')
        data.append(item)
    print(data)