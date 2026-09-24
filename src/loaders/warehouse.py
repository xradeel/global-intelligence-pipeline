import json
from pathlib import Path
from sqlalchemy.dialects.postgresql import insert as pg_insert

from src.warehouse.models import (
    DimCountry,
    FactCountryEconomics,
    FactNewsCoverage,
    FactWeatherObservation,
)
from src.warehouse.session import get_db_session


class WarehouseLoader:

  def read_json(self, file_path):
    path = Path(file_path)
    if not path.is_file():
      raise FileNotFoundError(f"File not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
      return json.load(f)

  def load_country(self, file_path):
    data = self.read_json(file_path)

    stmt = pg_insert(DimCountry).values(
        iso_a3=data.get("iso_a3"),
        iso_a2=data.get("iso_a2"),
        country_name=data.get("country_name"),
        region=data.get("region"),
        subregion=data.get("subregion"),
        government_type=data.get("government_type"),
        population=data.get("population"),
        area_sq_km=data.get("area_sq_km"),
        population_density_per_sq_km=data.get("population_density_per_sq_km"),
        capital_name=data.get("capital_name"),
        capital_lat=data.get("capital_lat"),
        capital_lng=data.get("capital_lng"),
        currency_code=data.get("currency_code"),
        currency_symbol=data.get("currency_symbol"),
        languages=data.get("languages"),
        gini_latest_year=data.get("gini_latest_year"),
        gini_latest_value=data.get("gini_latest_value"),
        is_g7=data.get("is_g7", False),
        is_g20=data.get("is_g20", False),
        is_nato=data.get("is_nato", False),
        is_brics=data.get("is_brics", False),
        is_commonwealth=data.get("is_commonwealth", False),
    )

    upsert_stmt = stmt.on_conflict_do_update(
        index_elements=[DimCountry.iso_a3],
        set_={
            "iso_a2": stmt.excluded.iso_a2,
            "country_name": stmt.excluded.country_name,
            "region": stmt.excluded.region,
            "subregion": stmt.excluded.subregion,
            "government_type": stmt.excluded.government_type,
            "population": stmt.excluded.population,
            "area_sq_km": stmt.excluded.area_sq_km,
            "population_density_per_sq_km": (
                stmt.excluded.population_density_per_sq_km
            ),
            "capital_name": stmt.excluded.capital_name,
            "capital_lat": stmt.excluded.capital_lat,
            "capital_lng": stmt.excluded.capital_lng,
            "currency_code": stmt.excluded.currency_code,
            "currency_symbol": stmt.excluded.currency_symbol,
            "languages": stmt.excluded.languages,
            "gini_latest_year": stmt.excluded.gini_latest_year,
            "gini_latest_value": stmt.excluded.gini_latest_value,
            "is_g7": stmt.excluded.is_g7,
            "is_g20": stmt.excluded.is_g20,
            "is_nato": stmt.excluded.is_nato,
            "is_brics": stmt.excluded.is_brics,
            "is_commonwealth": stmt.excluded.is_commonwealth,
            "updated_at": stmt.excluded.updated_at,
        },
    )

    with get_db_session() as session:
      session.execute(upsert_stmt)

    return data.get("iso_a3")

  def load_economics(self, file_path):
    data = self.read_json(file_path)

    stmt = pg_insert(FactCountryEconomics).values(
        country_code=data.get("country_code"),
        indicator_id=data.get("indicator_id"),
        indicator_name=data.get("indicator_name"),
        year=data.get("gdp_year"),
        gdp_usd=data.get("gdp_usd"),
    )

    upsert_stmt = stmt.on_conflict_do_update(
        constraint="uq_country_year_indicator",
        set_={
            "indicator_name": stmt.excluded.indicator_name,
            "gdp_usd": stmt.excluded.gdp_usd,
            "recorded_at": stmt.excluded.recorded_at,
        },
    )

    with get_db_session() as session:
      session.execute(upsert_stmt)

    return 1

  def load_weather(self, file_path, country_code="PAK"):
    data = self.read_json(file_path)

    stmt = pg_insert(FactWeatherObservation).values(
        country_code=country_code,
        observation_time=data.get("recorded_at"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
        elevation_m=data.get("elevation_m"),
        temperature_c=data.get("temperature_c"),
        relative_humidity_pct=data.get("relative_humidity_pct"),
        wind_speed_kmh=data.get("wind_speed_kmh"),
        dew_point_c=data.get("dew_point_c"),
        is_stagnant_air=data.get("is_stagnant_air"),
    )

    with get_db_session() as session:
      session.execute(stmt)

    return 1

  def load_news(self, file_path, target_country_code="PAK"):
    data = self.read_json(file_path)
    articles = data.get("articles", [])

    if not articles:
      return 0

    records = []
    for a in articles:
      if not a.get("url"):
        continue

      records.append({
          "target_country_code": target_country_code,
          "title": a.get("title", "").strip(),
          "domain": a.get("domain"),
          "language": a.get("language"),
          "source_country": a.get("source_country"),
          "published_at": a.get("published_at"),
          "url": a.get("url"),
      })

    if not records:
      return 0

    stmt = pg_insert(FactNewsCoverage).values(records)
    upsert_stmt = stmt.on_conflict_do_nothing(
        index_elements=[FactNewsCoverage.url]
    )

    with get_db_session() as session:
      session.execute(upsert_stmt)

    return len(records)