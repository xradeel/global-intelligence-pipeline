from src.validation.response import validate_json_list_file


path = "data/raw/countries/2026-09-23.json"
result = validate_json_list_file(path)
print(f"Validation result for {path}: {result}")