import json
from pathlib import Path
from typing import Any, List, Optional, Tuple


def validate_json_list_file(
    file_path: str,
):

    path = Path(file_path)

    if not path.is_file():
        return False, f"File not found: '{file_path}'"

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON syntax: {e}"
    except (OSError, UnicodeDecodeError) as e:
        return False, f"Could not read file: {e}"

    if not isinstance(data, (list, dict)):
        return (
            False,
            f"Expected a JSON list/array, but found: {type(data).__name__}",
        )

    return True, "Validation successful"
