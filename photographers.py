"""Функции для работы с фотографами.

Данные о фотографах хранятся в словаре:
    photographers[photographer_id] = {
        "name": str,
        "rating": float,
        "hourly_rate": float,
        "min_hours": int,
    }
"""


def add_photographer(
    photographers: dict[int, dict],
    name: str,
    rating: float,
    hourly_rate: float,
    min_hours: int,
) -> int:
    """Добавить фотографа в словарь photographers.

    Возвращает идентификатор созданного фотографа.
    """
    new_id = max(photographers.keys(), default=0) + 1
    photographers[new_id] = {
        "name": name,
        "rating": rating,
        "hourly_rate": hourly_rate,
        "min_hours": min_hours,
    }
    return new_id


def find_photographer(photographers: dict[int, dict], query: str) -> list[dict]:
    """Найти фотографов по подстроке имени."""
    query_lower = query.lower()
    return [
        {"id": pid, **data}
        for pid, data in photographers.items()
        if query_lower in data["name"].lower()
    ]


def sort_photographers_by_rating(
    photographers: dict[int, dict],
) -> list[dict]:
    """Отсортировать фотографов по рейтингу (по убыванию)."""
    return sorted(
        ({"id": pid, **data} for pid, data in photographers.items()),
        key=lambda p: p["rating"],
        reverse=True,
    )


def filter_photographers_by_rate(
    photographers: dict[int, dict], max_rate: float
) -> list[dict]:
    """Отобрать фотографов с почасовой ставкой не выше max_rate."""
    return [
        {"id": pid, **data}
        for pid, data in photographers.items()
        if data["hourly_rate"] <= max_rate
    ]