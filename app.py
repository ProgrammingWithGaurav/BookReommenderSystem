from fastapi import FastAPI
import joblib
import numpy as np
from pydantic import BaseModel
from typing import Union

class userInput(BaseModel):
    user_input: str

app = FastAPI()
popular_df = joblib.load('popular.joblib')
pt = joblib.load('pt.joblib')
books = joblib.load('books.joblib')
similarity_score = joblib.load('similarity_scores.joblib')

@app.get("/")
async def read_item():
    return {
     "book_name" : list(popular_df['Book-Title'].values),
     "author" : list(popular_df['Book-Author'].values),
     "images" : list(popular_df['Image-URL-M'].values),
     "votes" : list(popular_df['num_ratings']),
     "ratings" : list(popular_df['avg_rating'].values),
    }

@app.post("/recommend_books")
async def recommend(user_input: userInput):
    user_input = user_input['user_input']
    # index fetch
    index = np.where(pt.index==user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x:x[1], reverse=True)[1:6]
    
    data = []
    # looping items
    for i in similar_items:
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item = temp_df.drop_duplicates('Book-Title')
        data.append(item)
    return data