import os
import json
import pytest
from main import create_record, save_records, display_balance, load_records

# Предполагаем, что DATA_FILE_PATH установлен в 'data.json' для тестов
os.environ['DATA_FILE_PATH'] = 'data.txt'


def test_create_record():
    records = load_records()
    new_record = create_record("1", "2024-05-08", "income", 100.0, "Salary", records)
    assert new_record["id_record"] == 1
    assert new_record["date"] == "2024-05-08"
    assert new_record["category"] == "income"
    assert new_record["amount"] == 100.0
    assert new_record["description"] == "Salary"


def test_save_records():
    records = load_records()
    new_record = create_record("2", "2024-05-09", "expense", 50.0, "Groceries", records)
    records.append(new_record)
    save_records(records)
    loaded_records = load_records()
    assert len(loaded_records) == 1
    assert loaded_records[-1]["id_record"] == 2
    assert loaded_records[-1]["date"] == "2024-05-09"
    assert loaded_records[-1]["category"] == "expense"
    assert loaded_records[-1]["amount"] == 50.0
    assert loaded_records[-1]["description"] == "Groceries"
