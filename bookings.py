"""Функции для работы с бронированиями фотосессий.

bookings = [
    {
        "id": int,
        "photographer_id": int,
        "location_id": int,
        "client_name": str,
        "shoot_date": str,  # ISO-формат YYYY-MM-DD
        "hours": int,
        "need_makeup": bool,
        "total_cost": float,
    },
    ...
]
"""
from datetime import date


def is_photographer_available(
    bookings: list[dict], photographer_id: int, shoot_date: date
) -> bool:
    """Проверить, свободен ли фотограф на указанную дату."""
    iso_date = shoot_date.isoformat()
    return not any(
        b["photographer_id"] == photographer_id and b["shoot_date"] == iso_date
        for b in bookings
    )


def is_location_available(
    bookings: list[dict], location_id: int, shoot_date: date
) -> bool:
    """Проверить, свободна ли локация на указанную дату."""
    iso_date = shoot_date.isoformat()
    return not any(
        b["location_id"] == location_id and b["shoot_date"] == iso_date
        for b in bookings
    )


def calculate_base_cost(hours: int, hourly_rate: float, rent_price: float) -> float:
    """Базовая стоимость: работа фотографа + аренда локации."""
    return hours * hourly_rate + hours * rent_price


def calculate_total_cost(
    base_cost: float, need_makeup: bool, makeup_price: float = 2500.0
) -> float:
    """Итоговая стоимость с учётом дополнительных услуг."""
    if need_makeup:
        return base_cost + makeup_price
    return base_cost


def get_booking_status(
    is_available: bool, hours: int, min_allowed: int
) -> str:
    """Текстовый статус заказа (функция перенесена из ПР1)."""
    if not is_available:
        return "Бронирование невозможно: фотограф или локация заняты."
    if hours < min_allowed:
        return f"Бронирование невозможно: минимальная длительность — {min_allowed} ч."
    return "Бронирование подтверждено."


def create_booking(
    bookings: list[dict],
    photographer_id: int,
    location_id: int,
    client_name: str,
    shoot_date: date,
    hours: int,
    need_makeup: bool,
    photographers: dict[int, dict],
    locations: dict[int, dict],
) -> dict | None:
    """Создать новое бронирование.

    Возвращает словарь бронирования либо None, если создать нельзя.
    """
    photographer = photographers.get(photographer_id)
    location = locations.get(location_id)
    if photographer is None or location is None:
        return None

    available = (
        is_photographer_available(bookings, photographer_id, shoot_date)
        and is_location_available(bookings, location_id, shoot_date)
    )
    min_hours = photographer["min_hours"]

    if not available or hours < min_hours:
        return None

    base = calculate_base_cost(
        hours, photographer["hourly_rate"], location["rent_price"]
    )
    total = calculate_total_cost(base, need_makeup)

    new_id = max((b["id"] for b in bookings), default=0) + 1
    booking = {
        "id": new_id,
        "photographer_id": photographer_id,
        "location_id": location_id,
        "client_name": client_name,
        "shoot_date": shoot_date.isoformat(),
        "hours": hours,
        "need_makeup": need_makeup,
        "total_cost": total,
    }
    bookings.append(booking)
    return booking


def cancel_booking(bookings: list[dict], booking_id: int) -> bool:
    """Отменить бронирование по идентификатору."""
    for i, b in enumerate(bookings):
        if b["id"] == booking_id:
            bookings.pop(i)
            return True
    return False


def filter_bookings_by_client(
    bookings: list[dict], client_name: str
) -> list[dict]:
    """Отобрать бронирования по имени клиента."""
    query_lower = client_name.lower()
    return [b for b in bookings if query_lower in b["client_name"].lower()]


def sort_bookings_by_date(bookings: list[dict]) -> list[dict]:
    """Отсортировать бронирования по дате."""
    return sorted(bookings, key=lambda b: b["shoot_date"])