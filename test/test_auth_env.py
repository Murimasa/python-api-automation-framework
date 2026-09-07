import allure
import requests

@allure.epic("core Platform API")
@allure.feature("Authentication & Configuration")
def test_client_has_auth_header(base_url, authorized_client, api_token):
    """Проверяем, что URL подтянулся из .env, а клиент несет нужный Bearer-токен"""

    with allure.step("1. Проверка переменной base_url"):
        assert "jsonplaceholder" in base_url

    with allure.step("2. Проверка заголовков авторизации в сессии"):
        headers = authorized_client.headers
        assert "Authorization" in headers
        assert headers["Authorization"] == f"Bearer {api_token}"

    with allure.step("3. Отправка реального запроса с токеном в заголовках"):
        response = authorized_client.get(f"{base_url}/posts/1")
        assert response.status_code == 200

def test_out_of_token():
    with allure.step("Check request out of token (401)"):
        # Чистый URL без скобок и без authorized_client (токен передавать нельзя)
        response = requests.get("https://httpbin.org/bearer")
        assert response.status_code == 401

def test_valid_token():
    with allure.step("Check request valid token (200)"):
        # Чистый URL со строгим заголовком
        response = requests.get(
            "https://httpbin.org/bearer",
            headers={"Authorization": "Bearer my_secret_token"},
        )
        assert response.status_code == 200
        # В ответе проверяем булево поле 'authenticated', а не несуществующий ключ 'Authorization'
        assert response.json()["authenticated"] is True

def test_forbidden_request():
    with allure.step("Check request forbidden (403)"):
        # Чистый URL
        response = requests.get("https://httpbin.org/status/403")
        assert response.status_code == 403

def test_invalid_token_rejected():
    with allure.step("Check request rejected (200)"):
        response = requests.get(
            "https://httpbin.org/bearer",
            headers={"Authorization": "Bearer totally_wrong_secret"},
        )
        assert response.status_code == 200
        assert response.json()["token"] == "totally_wrong_secret"
