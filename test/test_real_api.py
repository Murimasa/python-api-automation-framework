import allure
import pytest

from core.data_generator import DataGenerator


@allure.feature("Users Management")
@allure.story("Read Single User")
def test_get_single_user(api_client):
    """Retrieve existing user by ID."""
    response = api_client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


@allure.feature("Users Management")
@allure.story("Negative ID Scenarios")
def test_user_not_found(api_client):
    """Ensure non-existent user returns 404 Not Found."""
    response = api_client.get("/users/9999")
    assert response.status_code == 404


@allure.feature("Users Management")
@allure.story("Create User")
def test_create_new_user(api_client):
    """Create a new user using dynamic test data."""
    payload = DataGenerator.generate_user_data()

    response = api_client.post("/users", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == payload["name"]
    assert data["username"] == payload["username"]
    assert "id" in data


@allure.feature("Users Management")
@allure.story("Update User")
def test_update_user(api_client):
    """Update existing user via PUT."""
    payload = {"name": "Updated Name"}
    response = api_client.put("/users/1", json=payload)
    assert response.status_code == 200
    assert response.json()["name"] == payload["name"]


@allure.feature("Users Management")
@allure.story("Delete User")
def test_delete_user(api_client):
    """Remove user by ID."""
    response = api_client.delete("/users/1")
    assert response.status_code == 200