from routes.relay import relay_status
from firebase.firebase_service import send_topic_notification

def apply_energy_decision(
    decision: str,
    avg_temp: float,
    avg_humidity: float,
    tomorrow_rain: int
):
    if decision == "START":
        relay_status["solar"] = "ON"
        relay_status["neighbour"] = "ON"

        send_topic_notification(
            title="☀️ Energy Sharing Started",
            body=(
                "No rain expected tomorrow.\n"
                f"Avg Temp: {avg_temp}°C\n"
                "Energy is now shared with neighbours."
            )
        )

    else:
        relay_status["neighbour"] = "OFF"

        send_topic_notification(
            title="🌧️ Energy Sharing Stopped",
            body=(
                "Rain expected tomorrow.\n"
                f"Avg Humidity: {avg_humidity}%\n"
                "Energy saved for home."
            )
        )
