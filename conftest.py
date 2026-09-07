import os
import pytest
import requests
import allure
from core.data_generator import DataGenerator
from dotenv import load_dotenv
from core.api_client import ApiClient

# Загружаем переменные из .env файла в окружение
load_dotenv()


@pytest.fixture(scope="session")
def base_url():
    """Берем BASE_URL из .env, а если его нет — используем дефолтный"""
    return os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")


@pytest.fixture(scope="session")
def api_token():
    """Берем секретный токен из .env"""
    return os.getenv("API_TOKEN")

@pytest.fixture(scope="session")
def api_client(base_url):
    """Session-wide API client instance."""
    token = os.getenv("API_TOKEN")
    client = ApiClient(base_url=base_url, token=token)
    yield client
    client.session.close()

@pytest.fixture(scope="session")
def authorized_client(api_token):
    """Клиент с преднастроенными заголовками авторизации"""
    session = requests.Session()
    # Подставляем стандартный заголовок авторизации по Bearer-токену
    session.headers.update({
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_token}"
    })
    yield session
    session.close()

@pytest.fixture(scope="session")
def custom_api(api_client):
    """Alias for backward compatibility."""
    return api_client

@pytest.fixture
def created_post(custom_api):
    """Setup: создаем пост перед тестом Teardown: удаляем пост после завершения теста."""
    # 1. SETUP
    payload = DataGenerator.generate_post_data()
    with allure.step("Setup: Создание тестового поста"):
        response = custom_api.post("/posts", json=payload)
        post_data = response.json()
        post_id = post_data["id"]

    # 2. Передаем данные в тест
    yield post_data

    # 3. TEARDOWN (выполнится гарантированно, даже если assert внутри теста упадет)
    with allure.step(f"Teardown: Удаление тестового поста с ID {post_id}"):
        custom_api.delete(f"/posts/{post_id}")