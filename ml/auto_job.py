from ml.ml_loader import RAIN_MODEL, LABEL_ENCODER, FEATURE_ORDER
from ml.weather_utils import get_tomorrow_weather, prepare_tomorrow_df
from ml.energy_controller import apply_energy_decision

CITY = "ramanathapuram"

def auto_ml_job():
    tomorrow_weather = get_tomorrow_weather(CITY)
    tomorrow_df = prepare_tomorrow_df(tomorrow_weather, LABEL_ENCODER)
    tomorrow_df = tomorrow_df[FEATURE_ORDER]

    tomorrow_rain = int(RAIN_MODEL.predict(tomorrow_df)[0])
    avg_temp = round(float(tomorrow_df["Temp"].iloc[0]), 2)
    avg_humidity = round(float(tomorrow_df["Humidity"].iloc[0]), 2)


    if tomorrow_rain == 1 and avg_temp < 22 or avg_humidity > 85:
        decision = "STOP"
    else:
        decision = "START"

    apply_energy_decision(
        decision=decision,
        avg_temp=avg_temp,
        avg_humidity=avg_humidity,
        tomorrow_rain=tomorrow_rain
    )

    print(f"[AUTO-ML] Decision={decision}")
