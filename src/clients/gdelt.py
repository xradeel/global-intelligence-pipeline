import io
import zipfile
import pandas as pd
import requests


class GdeltClient:

  LAST_UPDATE_URL = "http://data.gdeltproject.org/gdeltv2/lastupdate.txt"

  def call(self, country: str = "Pakistan"):
    # 1. Fetch the manifest of the latest 15-minute export
    resp = requests.get(self.LAST_UPDATE_URL, timeout=15)
    resp.raise_for_status()

    # The export URL is the first line of the manifest
    # Format: <size> <hash> <url>
    lines = resp.text.strip().split("\n")
    export_url = lines[0].split()[2]

    # 2. Download and unzip the CSV in-memory
    zip_resp = requests.get(export_url, timeout=30)
    zip_resp.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(zip_resp.content)) as z:
      csv_filename = z.namelist()[0]
      with z.open(csv_filename) as f:
        # Columns from GDELT 2.0 Event format
        df = pd.read_csv(
            f,
            sep="\t",
            header=None,
            usecols=[1, 6, 53, 57],
            names=[
                "date",
                "actor_country",
                "source_country",
                "source_url",
            ],
            dtype=str,
        )

    # 3. Filter for country mentions/events
    match = df[
        (df["actor_country"].str.contains(country[:3].upper(), na=False))
        | (df["source_country"].str.contains(country[:3].upper(), na=False))
    ].head(50)

    articles = []
    for _, row in match.iterrows():
      articles.append({
          "url": row["source_url"],
          "title": f"Event involving {country}",
          "source_country": row["source_country"],
          "published_at": str(row["date"]),
          "language": "en",
          "domain": (
              row["source_url"].split("/")[2]
              if pd.notna(row["source_url"])
              else None
          ),
      })

    return {"articles": articles}