"""Функции для работы с локациями.

locations[location_id] = {
    "name": str,
    "rent_price": float,
}
"""


def add_location(locations: dict[int, dict], name: str, rent_price: float) -> int:
    """Добавить локацию в словарь locations."""
    new_id = max(locations.keys(), default=0) + 1
    locations[new_id] = {"name": name, "rent_price": rent_price}
    return new_id


def find_location(locations: dict[int, dict], query: str) -> list[dict]:
    """Найти локации по подстроке названия."""
    query_lower = query.lower()
    return [
        {"id": lid, **data}
        for lid, data in locations.items()
        if query_lower in data["name"].lower()
    ]


def filter_locations_by_price(
    locations: dict[int, dict], max_price: float
) -> list[dict]:
    """Отобрать локации со стоимостью аренды не выше max_price."""
    return [
        {"id": lid, **data}
        for lid, data in locations.items()
        if data["rent_price"] <= max_price
    ]