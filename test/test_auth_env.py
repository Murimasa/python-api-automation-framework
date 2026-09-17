import allure


@allure.epic("Core Platform API")
@allure.feature("Authentication & Configuration")
class TestAuthConfiguration:

    @allure.story("Environment Variables & Session Auth")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_client_has_auth_header(self, base_url, api_client, api_token):
        """Verify BASE_URL and Bearer token injected into client session."""
        with allure.step("Verify base_url matches expected environment"):
            assert "jsonplaceholder" in base_url

        with allure.step("Verify default authorization headers in active session"):
            session_headers = api_client.session.headers
            assert "Authorization" in session_headers
            assert session_headers["Authorization"] == f"Bearer {api_token}"

        response = api_client.get("/posts/1")
        assert response.status_code == 200

    @allure.story("Unauthorized Access")
    @allure.severity(allure.severity_level.NORMAL)
    def test_out_of_token(self, api_client):
        """Verify 401 response without Authorization header."""
        # Clean request without default auth headers to external validation service
        response = api_client.get("https://httpbin.org/bearer", headers={"Authorization": None})
        assert response.status_code == 401

    @allure.story("Valid Bearer Token")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_valid_token(self, api_client):
        """Verify 200 response when valid Bearer token provided."""
        custom_token = "my_secret_token"
        response = api_client.get(
            "https://httpbin.org/bearer",
            headers={"Authorization": f"Bearer {custom_token}"},
        )
        assert response.status_code == 200
        assert response.json()["authenticated"] is True
        assert response.json()["token"] == custom_token

    @allure.story("Forbidden Request")
    @allure.severity(allure.severity_level.NORMAL)
    def test_forbidden_request(self, api_client):
        """Verify 403 Forbidden status response."""
        response = api_client.get("https://httpbin.org/status/403")
        assert response.status_code == 403

    @allure.story("Mock Token Echo")
    @allure.severity(allure.severity_level.MINOR)
    def test_token_echo_validation(self, api_client):
        """Verify httpbin reflects supplied Bearer token back in payload."""
        arbitrary_token = "totally_wrong_secret"
        response = api_client.get(
            "https://httpbin.org/bearer",
            headers={"Authorization": f"Bearer {arbitrary_token}"},
        )
        assert response.status_code == 200
        assert response.json()["token"] == arbitrary_token