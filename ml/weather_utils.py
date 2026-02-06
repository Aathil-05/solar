import requests
import pandas as pd
from datetime import datetime, timedelta, timezone

# ⚠️ Put your OpenWeather values here
BASE_URL = "https://api.openweathermap.org/data/2.5/"
API_KEY = "YOUR_OPENWEATHER_API_KEY"


# ---------- CURRENT WEATHER ----------
def get_current_weather(city: str) -> dict:
    url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric"
    res = requests.get(url, timeout=10)
    data = res.json()

    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "current_temp": round(data["main"]["temp"]),
        "feels_like": round(data["main"]["feels_like"]),
        "temp_min": round(data["main"]["temp_min"]),
        "temp_max": round(data["main"]["temp_max"]),
        "humidity": round(data["main"]["humidity"]),
        "pressure": data["main"]["pressure"],
        "description": data["weather"][0]["description"],
        "wind_gust_speed": data["wind"]["speed"],
        "wind_gust_dir": data["wind"]["deg"]
    }


# ---------- TOMORROW WEATHER (3-HOUR INTERVALS) ----------
def get_tomorrow_weather(city: str) -> list:
    url = f"{BASE_URL}forecast?q={city}&appid={API_KEY}&units=metric"
    res = requests.get(url, timeout=10)
    data = res.json()

    tomorrow_date = (datetime.now(timezone.utc) + timedelta(days=1)).date()

    return [
        x for x in data["list"]
        if datetime.fromtimestamp(x["dt"]).date() == tomorrow_date
    ]


# ---------- WIND DIRECTION ----------
def get_compass_direction(wind_deg: float) -> str:
    compass_points = [
        ("N", 0, 11.25), ("NNE", 11.25, 33.75), ("NE", 33.75, 56.25),
        ("ENE", 56.25, 78.75), ("E", 78.75, 101.25),
        ("ESE", 101.25, 123.75), ("SE", 123.75, 146.25),
        ("SSE", 146.25, 168.75), ("S", 168.75, 191.25),
        ("SSW", 191.25, 231.75), ("SW", 231.75, 254.25),
        ("W", 254.25, 281.25), ("WNW", 281.25, 303.75),
        ("NW", 303.75, 326.25), ("NNW", 326.25, 348.75)
    ]

    for point, start, end in compass_points:
        if start <= wind_deg < end:
            return point

    return "N"


# ---------- PREPARE TOMORROW DATAFRAME ----------
def prepare_tomorrow_df(tomorrow_data: list, label_encoder) -> pd.DataFrame:
    temps = [x["main"]["temp"] for x in tomorrow_data]
    hums = [x["main"]["humidity"] for x in tomorrow_data]
    pressures = [x["main"]["pressure"] for x in tomorrow_data]
    winds = [x["wind"]["speed"] for x in tomorrow_data]
    wind_dirs = [x["wind"].get("deg", 0) for x in tomorrow_data]

    avg_wind_deg = sum(wind_dirs) / len(wind_dirs)
    compass = get_compass_direction(avg_wind_deg)

    if compass in label_encoder.classes_:
        compass_encoded = label_encoder.transform([compass])[0]
    else:
        compass_encoded = -1

    return pd.DataFrame([{
        "MinTemp": min(temps),
        "MaxTemp": max(temps),
        "WindGustDir": compass_encoded,
        "WindGustSpeed": max(winds),
        "Humidity": sum(hums) / len(hums),
        "Pressure": sum(pressures) / len(pressures),
        "Temp": sum(temps) / len(temps)
    }])
