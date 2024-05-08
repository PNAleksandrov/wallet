import os
from dotenv import load_dotenv
import json
from typing import List, Optional

load_dotenv()

DATA_FILE_PATH = os.getenv("DATA_FILE_PATH")


def create_record(id_record: int, date: str, category: str, amount: float, description: str, records: List[dict]) \
        -> dict:
    """
        Создает новую запись с указанными параметрами и добавляет ее в список записей.

        :param id_record: Уникальный идентификатор записи.
        :param date: Дата записи.
        :param category: Категория записи (income/expense).
        :param amount: Сумма записи.
        :param description: Описание записи.
        :param records: Список всех записей.
        :return: Новая запись.
        """
    if any(record["id_record"] == int(id_record) for record in records):
        raise ValueError("Запись с таким ID уже существует.")
    record = {
        "id_record": int(id_record),
        "date": date,
        "category": category,
        "amount": float(amount),
        "description": description
    }
    return record


def save_records(records: List[dict]) -> None:
    """
    Сохраняет созданную запись в файл wallet_data.txt
    """
    with open(DATA_FILE_PATH, 'w') as file:
        json.dump(records, file)


def load_records() -> List[dict]:
    """
    Считывает записи из файла
    """
    try:
        with open(DATA_FILE_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def display_balance(records: List[dict]) -> None:
    """
    Показывает сумму доходов и сумму расходов, а также остаток средств
    """
    total_income = sum(record["amount"] for record in records if record["category"] == "income")
    total_expenses = sum(record["amount"] for record in records if record["category"] == "expense")
    balance = total_income - total_expenses
    print(f"Total Income: {total_income}")
    print(f"Total Expenses: {total_expenses}")
    print(f"Balance: {balance}")


def edit_record(id_record: int, date: str = None, category: str = None, amount: Optional[float] = None,
                description: str = None) -> str:
    """
    Позволяет редактировать уже созданные записи
    """
    records = load_records()
    for record in records:
        if record["id_record"] == int(id_record):
            if date:
                record["date"] = date
            if category:
                record["category"] = category
            if amount:
                record["amount"] = amount
            if description:
                record["description"] = description
            save_records(records)
            return f"Запись с ID {id_record} успешно отредактирована."
    return f"Запись с ID {id_record} не найдена."


def search_records(category: str = None, date: str = None, amount: Optional[float] = None):
    """
    Производит поиск записей по параметрам: категория, дата, сумма.
    """
    records = load_records()
    result = []
    for record in records:
        if category and record["category"] != category:
            continue
        if date and record["date"] != date:
            continue
        if amount and abs(float(record["amount"]) - float(amount)) > 0.01:
            continue
        result.append(record)
    return result


def main():
    """
    Функция возвращающая ваши действия из консоли
    например: показывает баланс при нажатии 1
    """
    records = load_records()
    while True:
        print("1. Баланс")
        print("2. Добавить запись")
        print("3. Редактировать запись")
        print("4. Найти запись")
        print("5. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            load_records()
            display_balance(records)
        elif choice == "2":
            id_record = input("Введите номер транзакции:")
            date = input("Введите дату (YYYY-MM-DD): ")
            category = input("Введите категорию (income/expense): ")
            amount = float(input("Введите сумму: "))
            description = input("Введите описание: ")
            try:
                records.append(create_record(id_record, date, category, amount, description, records))
                save_records(records)
            except ValueError as e:
                print(e)
        elif choice == "3":
            id_record = input("Введите номер транзакции для редактирования: ")
            date = input("Введите новую дату: ")
            category = input("Введите новую категорию (income/expense):")
            amount = float(input("Введите новую сумму: "))
            description = input("Введите новое описание:")
            print(edit_record(id_record, date, category, amount, description))
        elif choice == "4":
            category = input("Введите категорию для поиска (income/expense): ")
            date = input("Введите дату для поиска (YYYY-MM-DD): ")
            amount = input("Введите сумму для поиска: ")
            found_records = search_records(category=category, date=date, amount=amount)
            if found_records:
                for record in found_records:
                    print(record)
            else:
                print("Записи не найдены.")
        elif choice == "5":
            break
        else:
            print("Выберите другую цифру.")


if __name__ == "__main__":
    main()
