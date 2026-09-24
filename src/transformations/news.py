from collections import Counter
import json
from pathlib import Path
from typing import Any, Dict, List, Union


class TransformNews:
    
    def transform_gdelt_file(self, file_path):
        """Extracts news metrics, domain distribution, and clean headlines from GDELT JSON file."""
        path = Path(file_path)
        with open(path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        articles: List[Dict[str, Any]] = raw_data.get("articles", [])

        # Aggregate metrics
        total_articles = len(articles)
        source_countries = Counter(
            a.get("sourcecountry") for a in articles if a.get("sourcecountry")
        )
        languages = Counter(a.get("language") for a in articles if a.get("language"))

        # Structured list of articles
        processed_articles = []
        for a in articles:
            processed_articles.append({
                "title": a.get("title", "").strip(),
                "domain": a.get("domain"),
                "language": a.get("language"),
                "source_country": a.get("sourcecountry"),
                "published_at": a.get("seendate"),
                "url": a.get("url"),
            })

        return {
            "total_article_count": total_articles,
            "source_country_breakdown": dict(source_countries),
            "language_breakdown": dict(languages),
            "articles": processed_articles,
        }
