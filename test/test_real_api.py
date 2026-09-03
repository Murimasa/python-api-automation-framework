import pytest
import requests
from pygments.lexers import data


@pytest.fixture
def base_url():
    return "https://jsonplaceholder.typicode.com"


def test_get_single_user(base_url):
    """GET: получение пользователя"""
    response = requests.get(f"{base_url}/users/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_user_not_found(base_url):
    """GET 404: несуществующий пользователь"""
    response = requests.get(f"{base_url}/users/9999")
    assert response.status_code == 404


def test_create_new_user(base_url):
    """POST: создание нового пользователя"""
    payload = {
        "name": "Alex QA",
        "username": "alex_tester",
        "email": "alex@example.com"
    }
    response = requests.post(f"{base_url}/users", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == payload["name"]
    assert "id" in data

def test_delete_user(base_url):
    response = requests.delete(f"{base_url}/users/1")
    assert response.status_code == 200

def test_update_user(base_url):
    response = requests.put(f"{base_url}/users/1", json={"name": "New Name"} )
    assert response.status_code == 200