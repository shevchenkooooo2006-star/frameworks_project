"""Сохранение и загрузка данных проекта в JSON-файлах."""
import json
import os


def load_rooms(filename: str) -> dict:
    """Загрузить словарь из JSON-файла (общая функция)."""
    if not os.path.exists(filename):
        return {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Ошибка чтения {filename}: {e}")
        return {}


def save_rooms(filename: str, data: dict) -> None:
    """Сохранить словарь в JSON-файл (общая функция)."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"Ошибка записи {filename}: {e}")


def load_bookings(filename: str) -> list:
    """Загрузить список бронирований из JSON-файла."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Ошибка чтения {filename}: {e}")
        return []


def save_bookings(filename: str, bookings: list) -> None:
    """Сохранить список бронирований в JSON-файл."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(bookings, f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"Ошибка записи {filename}: {e}")


# Псевдонимы для удобства:
load_photographers = load_rooms
save_photographers = save_rooms
load_locations = load_rooms
save_locations = save_rooms