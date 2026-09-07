import allure
from core.data_generator import DataGenerator


@allure.epic("core Platform API")
@allure.feature("Dynamic Data Generation")
class TestDynamicPayloads:

    def test_create_post_with_faker(self, custom_api):
        """Создание поста с рандомным содержимым."""
        payload = DataGenerator.generate_post_data()

        response = custom_api.post("/posts", json=payload)

        assert response.status_code == 201
        response_data = response.json()
        assert response_data["title"] == payload["title"]
        assert response_data["body"] == payload["body"]
        assert response_data["userId"] == payload["userId"]

    def test_create_user_with_faker(self, custom_api):
        """Создание пользователя с реалистичным именем и почтой."""
        user_payload = DataGenerator.generate_user_data()

        response = custom_api.post("/users", json=user_payload)

        assert response.status_code == 201
        assert response.json()["email"] == user_payload["email"]