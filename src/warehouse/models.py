from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    ARRAY,
    func
)
from sqlalchemy.orm import Mapped, mapped_column
from src.warehouse.session import Base


class DimCountry(Base):
    __tablename__ = "dim_countries"

    iso_a3: Mapped[str] = mapped_column(String(3), primary_key=True)
    iso_a2: Mapped[str] = mapped_column(String(2), nullable=False)
    country_name: Mapped[str] = mapped_column(String(100), nullable=False)
    region: Mapped[Optional[str]] = mapped_column(String(50))
    subregion: Mapped[Optional[str]] = mapped_column(String(50))
    government_type: Mapped[Optional[str]] = mapped_column(String(100))
    population: Mapped[Optional[int]] = mapped_column(BigInteger)
    area_sq_km: Mapped[Optional[float]] = mapped_column(Numeric(12, 2))
    population_density_per_sq_km: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    capital_name: Mapped[Optional[str]] = mapped_column(String(100))
    capital_lat: Mapped[Optional[float]] = mapped_column(Numeric(8, 4))
    capital_lng: Mapped[Optional[float]] = mapped_column(Numeric(8, 4))
    currency_code: Mapped[Optional[str]] = mapped_column(String(3))
    currency_symbol: Mapped[Optional[str]] = mapped_column(String(10))
    languages: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String))
    gini_latest_year: Mapped[Optional[int]]
    gini_latest_value: Mapped[Optional[float]] = mapped_column(Numeric(5, 2))
    is_g7: Mapped[bool] = mapped_column(Boolean, default=False)
    is_g20: Mapped[bool] = mapped_column(Boolean, default=False)
    is_nato: Mapped[bool] = mapped_column(Boolean, default=False)
    is_brics: Mapped[bool] = mapped_column(Boolean, default=False)
    is_commonwealth: Mapped[bool] = mapped_column(Boolean, default=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )

class FactCountryEconomics(Base):
    __tablename__ = "fact_country_economics"
    __table_args__ = (
        UniqueConstraint("country_code", "year", "indicator_id", name="uq_country_year_indicator"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    country_code: Mapped[str] = mapped_column(String(3), index=True)
    indicator_id: Mapped[str] = mapped_column(String(50), nullable=False)
    indicator_name: Mapped[Optional[str]] = mapped_column(String(150))
    year: Mapped[int] = mapped_column(nullable=False)
    gdp_usd: Mapped[Optional[float]] = mapped_column(Numeric(18, 2))
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )

class FactWeatherObservation(Base):
    __tablename__ = "fact_weather_observations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    country_code: Mapped[str] = mapped_column(String(3), index=True)
    observation_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    latitude: Mapped[float] = mapped_column(Numeric(8, 4), nullable=False)
    longitude: Mapped[float] = mapped_column(Numeric(8, 4), nullable=False)
    elevation_m: Mapped[Optional[float]] = mapped_column(Numeric(6, 1))
    temperature_c: Mapped[Optional[float]] = mapped_column(Numeric(5, 2))
    relative_humidity_pct: Mapped[Optional[int]]
    wind_speed_kmh: Mapped[Optional[float]] = mapped_column(Numeric(5, 2))
    dew_point_c: Mapped[Optional[float]] = mapped_column(Numeric(5, 2))
    is_stagnant_air: Mapped[Optional[bool]] = mapped_column(Boolean)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )

class FactNewsCoverage(Base):
    __tablename__ = "fact_news_coverage"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    target_country_code: Mapped[str] = mapped_column(String(3), index=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    domain: Mapped[Optional[str]] = mapped_column(String(150))
    language: Mapped[Optional[str]] = mapped_column(String(50))
    source_country: Mapped[Optional[str]] = mapped_column(String(100))
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    url: Mapped[Optional[str]] = mapped_column(Text, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )