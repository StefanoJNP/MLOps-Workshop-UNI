from fastapi import FastAPI
import cloudpickle as cp
import pandas as pd
from schema import PredictionInput

app = FastAPI()

columns = [
    "cement",
    "blast_furnace_slag",
    "fly_ash",
    "water",
    "superplasticizer",
    "coarse_aggregate",
    "fine_aggregate",
    "age",
]


@app.get("/")
def read_root():
    return {"Hello": "UNI"}


@app.post("/predict")
def predict(data: PredictionInput):
    with open("model.pkl", "rb") as f:
        model = cp.load(f)

    X = pd.DataFrame([data.model_dump()], columns=columns)

    prediction = model.predict(X)
    return {"prediction": prediction[0]}
