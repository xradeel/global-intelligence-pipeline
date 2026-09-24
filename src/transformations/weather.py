import json
import math
from pathlib import Path

class TransformWeather:
    def transform_weather_file(self, file_path):

        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"Weather file not found at: {path}")

        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        current = raw.get("current", {})
        temp = current.get("temperature_2m")
        humidity = current.get("relative_humidity_2m")
        wind_speed = current.get("wind_speed_10m")

        # 1. Dew point estimation (Magnus-Tetens approximation)
        dew_point = None
        if temp is not None and humidity is not None:
            a, b = 17.27, 237.7
            alpha = ((a * temp) / (b + temp)) + math.log(humidity / 100.0)
            dew_point = round((b * alpha) / (a - alpha), 2)

        # 2. Atmospheric stagnation flag (high humidity + low wind)
        is_stagnant_air = (
            (wind_speed is not None and wind_speed < 5.0)
            and (humidity is not None and humidity > 75.0)
        )

        return {
            "recorded_at": current.get("time"),
            "latitude": raw.get("latitude"),
            "longitude": raw.get("longitude"),
            "elevation_m": raw.get("elevation"),
            "timezone": raw.get("timezone"),
            "temperature_c": temp,
            "relative_humidity_pct": humidity,
            "wind_speed_kmh": wind_speed,
            "dew_point_c": dew_point,
            "is_stagnant_air": is_stagnant_air,
        }

