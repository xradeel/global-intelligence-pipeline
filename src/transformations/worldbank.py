import json
from pathlib import Path

class TransformWorldBank:
    
    def transform_world_bank_file(self, file_path):
        path = Path(file_path)
        with open(path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        records = raw_data[1] if len(raw_data) > 1 else []
        if not records:
            raise ValueError(f"No records found in World Bank file: {path}")

        latest_record = records[0]
        return {
            "country_code": latest_record.get("countryiso3code"),
            "country_name": latest_record.get("country", {}).get("value"),
            "indicator_id": latest_record.get("indicator", {}).get("id"),
            "indicator_name": latest_record.get("indicator", {}).get("value"),
            "gdp_year": int(latest_record.get("date")),
            "gdp_usd": latest_record.get("value"),
        }
