
# main.py
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import requests
from datetime import datetime
import pymongo
import os

app = FastAPI()

# MongoDB Setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["weather_monitoring"]
summaries = db["daily_summaries"]

# API Configuration
API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"
CITIES = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]

# Convert temperature from Kelvin to Celsius
def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

# Fetch weather data for a given city
def fetch_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return {
        "main": data["weather"][0]["main"],
        "temp": kelvin_to_celsius(data["main"]["temp"]),
        "feels_like": kelvin_to_celsius(data["main"]["feels_like"]),
        "dt": datetime.fromtimestamp(data["dt"])
    }

# Update weather data and store daily summary in MongoDB
@app.get("/update_weather")
def update_weather(background_tasks: BackgroundTasks):
    background_tasks.add_task(process_weather_data)
    return {"status": "Processing weather data in the background"}

def process_weather_data():
    daily_data = []
    for city in CITIES:
        data = fetch_weather_data(city)
        daily_data.append(data)

    # Calculate daily aggregates
    max_temp = max(d["temp"] for d in daily_data)
    min_temp = min(d["temp"] for d in daily_data)
    avg_temp = sum(d["temp"] for d in daily_data) / len(daily_data)
    dominant_weather = max(set(d["main"] for d in daily_data), key=daily_data.count)

    # Insert daily summary into MongoDB
    summaries.insert_one({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "average_temp": avg_temp,
        "max_temp": max_temp,
        "min_temp": min_temp,
        "dominant_weather": dominant_weather,
        "data": daily_data
    })

# Endpoint to retrieve daily summaries
@app.get("/summaries")
def get_summaries():
    return list(summaries.find({}, {"_id": 0}))

# Alert Configuration
class AlertConfig(BaseModel):
    temperature_threshold: float
    consecutive_updates: int

@app.post("/set_alert")
def set_alert(config: AlertConfig):
    # Future logic to set temperature alerts
    return {"status": "Alert set with the following configuration", "config": config.dict()}
