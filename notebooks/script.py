import requests

url = "http://localhost:8000/predict"

data = {
    "cement": 540.0,
    "blast_furnace_slag": 0.0,
    "fly_ash": 0.0,
    "water": 162.0,
    "superplasticizer": 2.5,
    "coarse_aggregate": 1000.0,
    "fine_aggregate": 700.0,
    "age": 28.0,
}

response = requests.post(url, json=data)
print(response.json())
