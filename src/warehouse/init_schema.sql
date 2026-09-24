-- 1. Dimension Table: Countries
CREATE TABLE IF NOT EXISTS dim_countries (
    iso_a3 VARCHAR(3) PRIMARY KEY,
    iso_a2 VARCHAR(2) NOT NULL,
    country_name VARCHAR(100) NOT NULL,
    region VARCHAR(50),
    subregion VARCHAR(50),
    government_type VARCHAR(100),
    population BIGINT,
    area_sq_km NUMERIC(12, 2),
    population_density_per_sq_km NUMERIC(10, 2),
    capital_name VARCHAR(100),
    capital_lat NUMERIC(8, 4),
    capital_lng NUMERIC(8, 4),
    currency_code VARCHAR(3),
    currency_symbol VARCHAR(10),
    languages TEXT[],
    gini_latest_year INT,
    gini_latest_value NUMERIC(5, 2),
    is_g7 BOOLEAN DEFAULT FALSE,
    is_g20 BOOLEAN DEFAULT FALSE,
    is_nato BOOLEAN DEFAULT FALSE,
    is_brics BOOLEAN DEFAULT FALSE,
    is_commonwealth BOOLEAN DEFAULT FALSE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Fact Table: Economic Indicators (World Bank)
CREATE TABLE IF NOT EXISTS fact_country_economics (
    id SERIAL PRIMARY KEY,
    country_code VARCHAR(3) REFERENCES dim_countries(iso_a3),
    indicator_id VARCHAR(50) NOT NULL,
    indicator_name VARCHAR(150),
    year INT NOT NULL,
    gdp_usd NUMERIC(18, 2),
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_country_year_indicator UNIQUE (country_code, year, indicator_id)
);

-- 3. Fact Table: Real-Time Weather (Open-Meteo)
CREATE TABLE IF NOT EXISTS fact_weather_observations (
    id SERIAL PRIMARY KEY,
    country_code VARCHAR(3) REFERENCES dim_countries(iso_a3),
    observation_time TIMESTAMP NOT NULL,
    latitude NUMERIC(8, 4) NOT NULL,
    longitude NUMERIC(8, 4) NOT NULL,
    elevation_m NUMERIC(6, 1),
    temperature_c NUMERIC(5, 2),
    relative_humidity_pct INT,
    wind_speed_kmh NUMERIC(5, 2),
    dew_point_c NUMERIC(5, 2),
    is_stagnant_air BOOLEAN,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Fact Table: News Articles (GDELT)
CREATE TABLE IF NOT EXISTS fact_news_coverage (
    id SERIAL PRIMARY KEY,
    target_country_code VARCHAR(3) REFERENCES dim_countries(iso_a3),
    title TEXT NOT NULL,
    domain VARCHAR(150),
    language VARCHAR(50),
    source_country VARCHAR(100),
    published_at TIMESTAMP,
    url TEXT UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
