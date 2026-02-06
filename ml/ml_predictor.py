import pandas as pd
from ml.ml_loader import RAIN_MODEL, LABEL_ENCODER, FEATURE_ORDER
from ml.weather_utils import get_compass_direction

def predict_rain_from_weather(weather_dict):
    wind_deg = weather_dict["wind_gust_dir"] % 360
    compass = get_compass_direction(wind_deg)

    if compass in LABEL_ENCODER.classes_:
        compass_encoded = LABEL_ENCODER.transform([compass])[0]
    else:
        compass_encoded = -1

    df = pd.DataFrame([{
        'MinTemp': weather_dict['temp_min'],
        'MaxTemp': weather_dict['temp_max'],
        'WindGustDir': compass_encoded,
        'WindGustSpeed': weather_dict['wind_gust_speed'],
        'Humidity': weather_dict['humidity'],
        'Pressure': weather_dict['pressure'],
        'Temp': weather_dict['current_temp']
    }])

    df = df[FEATURE_ORDER]

    return int(RAIN_MODEL.predict(df)[0])


def predict_tomorrow_rain(tomorrow_df):
    tomorrow_df = tomorrow_df[FEATURE_ORDER]
    return int(RAIN_MODEL.predict(tomorrow_df)[0])
