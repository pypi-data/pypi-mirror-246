from pathlib import Path
import json

THIS_DIR = Path(__file__).parent
CITIES_JSON_FPATH = THIS_DIR / "./cities.json"


def is_city_capital(city: str, state: str) -> bool:
    cities_json_content =CITIES_JSON_FPATH.read_text()
    cities = json.loads(cities_json_content)
    matching_cities = [c for c in cities if c["city"] == city and c["state"] == state]
    matched_city = matching_cities[0] if len(matching_cities) > 0 else None
    return matched_city["capital"]


if __name__ == "__main__":
    print(is_city_capital("Phoenix", "Arizona"))
