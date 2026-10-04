# Вспомогательные функции для безопасного ввода данных.
from datetime import date, datetime


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число.

    При некорректном вводе запрос повторяется.
    """
    while True: # бесконечный цикл, пока не получится число
        try:
            return int(input(prompt)) # попытка преобразования ввода в int
        except ValueError: # обработка ошибки, если не получилось
            print("Ошибка: введите целое число.")


def input_float(prompt: str) -> float:
    """Запросить у пользователя число с плавающей точкой."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Ошибка: введите число.")


def input_date(prompt: str) -> date:
    """Запросить у пользователя дату в формате ДД.ММ.ГГГГ."""
    while True:
        try:
            return datetime.strptime(input(prompt), "%d.%m.%Y").date()
        except ValueError:
            print("Ошибка: введите дату в формате ДД.ММ.ГГГГ.")


def input_yes_no(prompt: str) -> bool:
    """Запросить у пользователя ответ да/нет."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("да", "д", "yes", "y"):
            return True
        if answer in ("нет", "н", "no", "n"):
            return False
        print("Ошибка: введите 'да' или 'нет'.")