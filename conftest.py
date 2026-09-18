import os
import allure
import uuid
from dotenv import load_dotenv
import pytest
import requests

from core.api_client import ApiClient
from core.data_generator import DataGenerator
from core.db_client import DatabaseClient
load_dotenv()


@pytest.fixture(scope="session")
def base_url() -> str:
    """Retrieve BASE_URL from environment or fallback to default."""
    return os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")


@pytest.fixture(scope="session")
def api_token() -> str | None:
    """Retrieve secret API token from environment."""
    return os.getenv("API_TOKEN")


@pytest.fixture(scope="session")
def api_client(base_url: str, api_token: str | None) -> ApiClient:
    """Session-wide ApiClient instance with automatic session cleanup."""
    client_instance = ApiClient(base_url=base_url, token=api_token)
    yield client_instance
    client_instance.session.close()


@pytest.fixture(scope="session")
def client(api_client: ApiClient) -> ApiClient:
    """Alias for api_client fixture."""
    return api_client


@pytest.fixture(scope="session")
def custom_api(api_client: ApiClient) -> ApiClient:
    """Backward compatibility alias for api_client."""
    return api_client


@pytest.fixture(scope="session")
def authorized_client(api_token: str | None) -> requests.Session:
    """Raw requests.Session configured with Bearer token authorization."""
    session = requests.Session()
    session.headers.update(
        {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_token}",
        }
    )
    yield session
    session.close()


@pytest.fixture
def created_post(client: ApiClient):
    """Setup and teardown fixture for creating and deleting a temporary post."""
    payload = DataGenerator.generate_post_data()
    with allure.step("Setup: Create temporary post"):
        response = client.post("/posts", json=payload)
        post_data = response.json()
        post_id = post_data["id"]

    yield post_data

    with allure.step(f"Teardown: Delete temporary post with ID {post_id}"):
        client.delete(f"/posts/{post_id}")


@pytest.fixture
def db():
    """Provides an isolated database instance per test, avoiding file lock conflicts."""
    # Generate unique database file name for each test iteration
    db_file = f"test_{uuid.uuid4().hex[:8]}.db"

    # Setup
    client = DatabaseClient(db_file).connect()
    client.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        );
    """)
    client.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            item_title TEXT NOT NULL,
            amount REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        );
    """)

    yield client

    # Teardown
    client.close()
    if os.path.exists(db_file):
        try:
            os.remove(db_file)
        except PermissionError:
            pass  # Fallback if Windows filesystem releases the file handle with a delay
