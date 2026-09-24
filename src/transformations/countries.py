import json
from pathlib import Path
from typing import Any, Dict, Union

class TransformCountries:

    def transform_country_file(self, file_path):

        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"Country raw file not found at: {path}")

        with open(path, "r", encoding="utf-8") as f:
            raw_json = json.load(f)

        objects = raw_json.get("data", {}).get("objects", [])
        if not objects:
            raise ValueError(f"No country data found in {path}")

        country = objects[0]

        capitals = country.get("capitals", [{}])
        primary_capital = capitals[0] if capitals else {}
        cap_coords = primary_capital.get("coordinates", {})

        # 2. Economy & Gini coefficient
        gini_dict = country.get("economy", {}).get("gini_coefficient", {})
        latest_gini_year = (
            max(gini_dict.keys(), key=int) if gini_dict else None
        )
        latest_gini_value = (
            gini_dict[latest_gini_year] if latest_gini_year else None
        )

        # 3. Demographics & Density
        population = country.get("population", 0)
        area_sq_km = country.get("area", {}).get("kilometers", 0)
        pop_density = round(population / area_sq_km, 2) if area_sq_km else None

        # 4. Currency
        currencies = country.get("currencies", [{}])
        primary_curr = currencies[0] if currencies else {}

        # 5. Geopolitical memberships
        memberships = country.get("memberships", {})

        res = {
            "country_name": country.get("names", {}).get("common"),
            "iso_a3": country.get("codes", {}).get("alpha_3"),
            "iso_a2": country.get("codes", {}).get("alpha_2"),
            "region": country.get("region"),
            "subregion": country.get("subregion"),
            "government_type": country.get("government_type"),
            "population": population,
            "area_sq_km": area_sq_km,
            "population_density_per_sq_km": pop_density,
            "capital_name": primary_capital.get("name"),
            "capital_lat": cap_coords.get("lat"),
            "capital_lng": cap_coords.get("lng"),
            "currency_code": primary_curr.get("code"),
            "currency_symbol": primary_curr.get("symbol"),
            "languages": [
                lang.get("name") for lang in country.get("languages", [])
            ],
            "gini_latest_year": int(latest_gini_year) if latest_gini_year else None,
            "gini_latest_value": latest_gini_value,
            "is_g7": memberships.get("g7", False),
            "is_g20": memberships.get("g20", False),
            "is_nato": memberships.get("nato", False),
            "is_brics": memberships.get("brics", False),
            "is_commonwealth": memberships.get("commonwealth", False),
        }
        print(res)
        return res



TransformCountries().transform_country_file("data/raw/countries/2026-09-23.json")