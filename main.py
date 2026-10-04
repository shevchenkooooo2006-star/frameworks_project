#Сервис организации фотосессий.

#Точка входа: меню приложения и вызов функций проекта.


from datetime import date

from bookings import (
    create_booking,
    cancel_booking,
    get_booking_status,
    is_photographer_available,
    is_location_available,
    filter_bookings_by_client,
    sort_bookings_by_date,
)
from photographers import (
    add_photographer,
    find_photographer,
    sort_photographers_by_rating,
    filter_photographers_by_rate,
)
from locations import add_location, find_location, filter_locations_by_price
from storage import (
    load_photographers, save_photographers,
    load_locations, save_locations,
    load_bookings, save_bookings,
)
from utils import input_int, input_float, input_date, input_yes_no

PHOTOGRAPHERS_FILE = "data/photographers.json"
LOCATIONS_FILE = "data/locations.json"
BOOKINGS_FILE = "data/bookings.json"


def show_photographers(photographers: dict[int, dict]) -> None:
    """Вывести список фотографов."""
    if not photographers:
        print("Список фотографов пуст.")
        return
    print("\n--- Фотографы ---")
    for pid, p in photographers.items():
        print(f"[{pid}] {p['name']} | рейтинг {p['rating']} | "
              f"{p['hourly_rate']:.0f} руб./ч | мин. {p['min_hours']} ч.")


def show_locations(locations: dict[int, dict]) -> None:
    """Вывести список локаций."""
    if not locations:
        print("Список локаций пуст.")
        return
    print("\n--- Локации ---")
    for lid, loc in locations.items():
        print(f"[{lid}] {loc['name']} | {loc['rent_price']:.0f} руб./ч")


def show_bookings(
    bookings: list[dict],
    photographers: dict[int, dict],
    locations: dict[int, dict],
) -> None:
    """Вывести список бронирований."""
    if not bookings:
        print("Бронирований нет.")
        return
    print("\n--- Бронирования ---")
    for b in bookings:
        ph = photographers.get(b["photographer_id"], {}).get("name", "?")
        loc = locations.get(b["location_id"], {}).get("name", "?")
        print(
            f"[{b['id']}] {b['client_name']} | {b['shoot_date']} | "
            f"{b['hours']} ч. | фотограф: {ph} | локация: {loc} | "
            f"итого: {b['total_cost']:.2f} руб."
        )


def menu_create_booking(
    photographers: dict[int, dict],
    locations: dict[int, dict],
    bookings: list[dict],
) -> None:
    """Диалог создания бронирования."""
    show_photographers(photographers)
    show_locations(locations)
    photographer_id = input_int("ID фотографа: ")
    location_id = input_int("ID локации: ")
    client_name = input("Имя клиента: ").strip()
    shoot_date = input_date("Дата съёмки (ДД.ММ.ГГГГ): ")
    hours = input_int("Длительность, ч: ")
    need_makeup = input_yes_no("Нужен визажист? (да/нет): ")

    booking = create_booking(
        bookings, photographer_id, location_id, client_name,
        shoot_date, hours, need_makeup, photographers, locations,
    )
    if booking:
        print(f"Бронирование создано. Итого: {booking['total_cost']:.2f} руб.")
    else:
        print("Бронирование не создано: проверьте доступность и минимальную длительность.")


def main() -> None:
    """Точка запуска приложения."""
    photographers = load_photographers(PHOTOGRAPHERS_FILE)
    locations = load_locations(LOCATIONS_FILE)
    bookings = load_bookings(BOOKINGS_FILE)

    # Начальные данные, если файлы пусты
    if not photographers:
        add_photographer(photographers, "Анна Смирнова", 4.8, 3500.0, 2)
    if not locations:
        add_location(locations, "Студия «Свет»", 1500.0)

    while True:
        print("\n=== Сервис организации фотосессий ===")
        print("1. Показать фотографов")
        print("2. Показать локации")
        print("3. Показать бронирования")
        print("4. Найти фотографа по имени")
        print("5. Отсортировать фотографов по рейтингу")
        print("6. Создать бронирование")
        print("7. Отменить бронирование")
        print("8. Найти бронирования по клиенту")
        print("9. Проверить доступность фотографа на дату")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_photographers(photographers)
        elif choice == "2":
            show_locations(locations)
        elif choice == "3":
            show_bookings(bookings, photographers, locations)
        elif choice == "4":
            q = input("Подстрока имени: ")
            for p in find_photographer(photographers, q):
                print(p)
        elif choice == "5":
            for p in sort_photographers_by_rating(photographers):
                print(p)
        elif choice == "6":
            menu_create_booking(photographers, locations, bookings)
        elif choice == "7":
            bid = input_int("ID бронирования для отмены: ")
            print("Отменено." if cancel_booking(bookings, bid) else "Не найдено.")
        elif choice == "8":
            q = input("Имя клиента: ")
            for b in filter_bookings_by_client(bookings, q):
                print(b)
        elif choice == "9":
            pid = input_int("ID фотографа: ")
            d = input_date("Дата (ДД.ММ.ГГГГ): ")
            ok = is_photographer_available(bookings, pid, d)
            print(get_booking_status(ok, 2, 2))
        elif choice == "0":
            save_photographers(PHOTOGRAPHERS_FILE, photographers)
            save_locations(LOCATIONS_FILE, locations)
            save_bookings(BOOKINGS_FILE, bookings)
            print("Данные сохранены. До свидания!")
            break
        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    main()