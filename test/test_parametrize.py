import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


# 1. Задаем параметры: имя переменной ("user_id") и список значений ([1, 2, 3])
@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_get_multiple_users(user_id):
    """Один тест, который проверит сразу трех пользователей"""
    response = requests.get(f"{BASE_URL}/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["id"] == user_id


# Передаем пары: (входной_id, ожидаемый_статус)
@pytest.mark.parametrize("invalid_id, expected_status", [
    (0, 404),
    (9999, 404),
    (-1, 404)
])
def test_get_user_invalid_ids(invalid_id, expected_status):
    """Проверяем граничные и невалидные ID"""
    response = requests.get(f"{BASE_URL}/users/{invalid_id}")

    # Сравниваем статус ответа с ожидаемым из таблицы параметров
    assert response.status_code == expected_status