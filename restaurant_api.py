from copyreg import pickle
import string
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder


app = FastAPI()

class preferencesItem(BaseModel):
    menu: str
    price: int
    location: str
    
with open('restaurant_lr_model.pkl', 'rb') as file:
    model = pickle.load(file)

@app.post('/')
async def restaurant_endpoint(item:preferencesItem):
    df = pd.DataFrame([item.dict().values()], columns=item.dict().keys())
    le = LabelEncoder()
    for column in item.dict().keys():
        df[column] = le.fit_transform(df[column])
    prediction = model.predict(df)
    if prediction == 0:
        return {"Recommended Restaurant":"MadChef"}
    else:
        return {"Recommended Restaurant":"PizzaHutBD"}