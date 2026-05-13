from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
import joblib

app = FastAPI()

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)

model = joblib.load("models/lgbm_model.pkl")


@app.get("/")
def home():

    return {

        "message":
            "Zomato ETA AI Backend Running"

    }


@app.post("/predict")
def predict(data: dict):

    distance_km = float(data["distance_km"])

    traffic_score = float(data["traffic_score"])

    weather_score = float(data["weather_score"])

    is_rush_hour = int(data["is_rush_hour"])

    prep_time = float(data["prep_time"])

    is_weekend = int(data["is_weekend"])

    city_avg_eta = float(data["city_avg_eta"])


    input_df = pd.DataFrame([{

        "Delivery_person_Age":
            28,

        "Delivery_person_Ratings":
            4.5,

        "Vehicle_condition":
            2,

        "multiple_deliveries":
            1,

        "Weather_conditions":
            int(weather_score),

        "Road_traffic_density":
            int(traffic_score),

        "Type_of_order":
            1,

        "Type_of_vehicle":
            1,

        "Festival":
            0,

        "City":
            1,

        "distance_km":
            distance_km,

        "order_hour": int(data.get("order_hour", 20)),

        "is_rush_hour":
            is_rush_hour,

        "prep_time":
            prep_time,

        "traffic_score":
            traffic_score,

        "weather_score":
            weather_score,

        "traffic_distance":
            (
                traffic_score
                *
                distance_km
            ),

        "is_weekend":
            is_weekend,

        "city_avg_eta":
            city_avg_eta

    }])


    prediction = model.predict(input_df)[0]


    prediction += (
        traffic_score * 3
    )

    prediction += (
        distance_km * 0.8
    )

    if is_rush_hour == 1:

        prediction += 4


    if prediction < 10:

        prediction = 10


    return {

        "predicted_eta":
            round(float(prediction), 2)

    }