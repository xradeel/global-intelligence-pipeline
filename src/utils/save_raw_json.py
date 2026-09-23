import json
from pathlib import Path


def save_raw(data, path):
    path = Path(path)

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as file:
        json.dump(data, file, indent=2)