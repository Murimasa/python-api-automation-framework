import allure

from core.data_generator import DataGenerator
from core.schemas import UserSchema


@allure.epic("Core Platform API")
@allure.feature("User Management")
class TestUserAPI:

    @allure.story("Get user profile")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_success(self, api_client):
        """Retrieve user profile and validate essential contract fields."""
        response = api_client.get("/users/1")
        assert response.status_code == 200

        with allure.step("Validate user schema and identity"):
            user = UserSchema.model_validate(response.json())
            assert user.id == 1
            assert user.username == "Bret"

    @allure.story("Create user profile")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_user(self, api_client):
        """Create new user profile via POST using generated payload."""
        payload = DataGenerator.generate_user_data()

        response = api_client.post("/users", json=payload)
        assert response.status_code == 201

        with allure.step("Validate response contains submitted user properties"):
            data = response.json()
            assert data["name"] == payload["name"]
            assert data["username"] == payload["username"]
            assert "id" in data