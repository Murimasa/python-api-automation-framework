import allure
import json


@allure.epic("Core Platform API")
@allure.feature("User Management")
class TestUserAPI:

    @allure.story("Get user profile")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_success(self, base_url, api_client):
        """Успешное получение данных пользователя с проверкой полей"""

        with allure.step("1. Отправка GET-запроса на получение юзера с ID=1"):
            response = api_client.get(f"{base_url}/users/1")

        with allure.step("2. Проверка HTTP статус-кода"):
            assert response.status_code == 200

        with allure.step("3. Валидация содержимого ответа"):
            user_data = response.json()
            assert user_data["id"] == 1
            assert "username" in user_data

    @allure.story("Create user profile")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_user(self, base_url, api_client):
        """Создание нового пользователя через POST"""

        payload = {"name": "Senior QA", "username": "senior_tester"}

        with allure.step("1. Отправка POST-запроса с payload"):
            response = api_client.post(f"{base_url}/users", json=payload)

        with allure.step("2. Проверка создания сущности (201 Created)"):
            assert response.status_code == 201

        with allure.step("3. Проверка возвращенных сервером данных"):
            assert response.json()["name"] == payload["name"]

def test_create_user_with_attachments(base_url, api_client):
    """Тест с логированием тела запроса и ответа прямо в отчет Allure"""
    payload = {"name": "Senior Automation QA", "role": "Lead"}

    with allure.step("1. Подготовка и отправка данных"):
        # Прикрепляем отправляемый payload в виде JSON к отчету
        allure.attach(
            json.dumps(payload, indent=2),
            name="Request Payload",
            attachment_type=allure.attachment_type.JSON,
        )

        response = api_client.post(f"{base_url}/users", json=payload)

    with allure.step("2. Логирование ответа сервера"):
        # Прикрепляем ответ сервера
        allure.attach(
            json.dumps(response.json(), indent=2),
            name="Response Body",
            attachment_type=allure.attachment_type.JSON,
        )
        assert response.status_code == 201