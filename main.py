"""Сервис организации фотосессий.

Начальный сценарий: проверка возможности бронирования фотосессии,
расчёт итоговой стоимости и формирование статуса заказа.
"""

from datetime import date

# Данные о фотографе и услуге (простые типы данных)
photographer_name = "Анна Смирнова"
photographer_rating = 4.8
hourly_rate = 3500.0          # стоимость съёмки, руб./ч
min_hours = 2                 # минимальная длительность съёмки, ч
is_photographer_available = True

# Данные о локации
location_name = "Студия «Свет»"
location_rent_price = 1500.0  # стоимость аренды, руб./ч
is_location_available = True

# Параметры заказа
client_name = "Иван Петров"
shoot_date = date(2026, 10, 5)
shoot_hours = 3               # желаемая длительность съёмки, ч
need_makeup = True            # нужен ли визажист
makeup_price = 2500.0         # стоимость услуг визажиста, руб.


def check_availability(photographer_ok: bool, location_ok: bool) -> bool:
    """Проверяет доступность фотографа и локации на выбранную дату."""
    return photographer_ok and location_ok


def calculate_base_cost(hours: int, rate: float, location_price: float) -> float:
    """Рассчитывает базовую стоимость съёмки: работа фотографа + аренда локации."""
    photographer_cost = hours * rate
    location_cost = hours * location_price
    return photographer_cost + location_cost


def calculate_total_cost(base_cost: float, with_makeup: bool, makeup_cost: float) -> float:
    """Рассчитывает итоговую стоимость с учётом дополнительных услуг."""
    if with_makeup:
        return base_cost + makeup_cost
    return base_cost


def get_booking_status(is_available: bool, hours: int, min_allowed: int) -> str:
    """Формирует текстовый статус заказа."""
    if not is_available:
        return "Бронирование невозможно: фотограф или локация заняты."
    if hours < min_allowed:
        return f"Бронирование невозможно: минимальная длительность — {min_allowed} ч."
    return "Бронирование подтверждено."


def main() -> None:
    """Основной сценарий: проверка, расчёт и вывод результата."""
    available = check_availability(is_photographer_available, is_location_available)

    print("=" * 50)
    print("СЕРВИС ОРГАНИЗАЦИИ ФОТОСЕССИЙ")
    print("=" * 50)
    print(f"Клиент:        {client_name}")
    print(f"Фотограф:      {photographer_name} (рейтинг {photographer_rating})")
    print(f"Локация:       {location_name}")
    print(f"Дата съёмки:   {shoot_date}")
    print(f"Длительность:  {shoot_hours} ч.")
    print("-" * 50)

    status = get_booking_status(available, shoot_hours, min_hours)
    print(f"Статус: {status}")

    if available and shoot_hours >= min_hours:
        base_cost = calculate_base_cost(shoot_hours, hourly_rate, location_rent_price)
        total_cost = calculate_total_cost(base_cost, need_makeup, makeup_price)
        print(f"Базовая стоимость:   {base_cost:.2f} руб.")
        if need_makeup:
            print(f"Услуги визажиста:    {makeup_price:.2f} руб.")
        print(f"ИТОГО к оплате:      {total_cost:.2f} руб.")

    print("=" * 50)
if __name__ == "__main__":
    main()
