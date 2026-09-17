import allure
import pytest

from core.schemas import UserSchema


@allure.feature("Users Management")
@allure.story("Contract Validation")
def test_user_schema_contract(api_client):
    """Ensure GET /users/1 matches the strict UserSchema contract."""
    response = api_client.get("/users/1")
    assert response.status_code == 200

    user_data = UserSchema.model_validate(response.json())
    assert user_data.id == 1