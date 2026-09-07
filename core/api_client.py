import json
import os
import allure
import requests


class ApiClient:

    def __init__(self, base_url: str = None, token: str = None):
        self.base_url = (
            base_url or os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")
        ).rstrip("/")
        self.session = requests.Session()

        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})

    def _send_request(self, method: str, endpoint: str, **kwargs):
        """Unified request dispatcher with automatic Allure reporting."""
        # Handle both relative endpoints and absolute URLs safely
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            url = endpoint
        else:
            normalized_endpoint = (
                endpoint if endpoint.startswith("/") else f"/{endpoint}"
            )
            url = f"{self.base_url}{normalized_endpoint}"

        with allure.step(f"{method.upper()} {endpoint}"):
            # Log payload if present
            if "json" in kwargs and kwargs["json"] is not None:
                allure.attach(
                    json.dumps(kwargs["json"], indent=2, ensure_ascii=False),
                    name="Request JSON Body",
                    attachment_type=allure.attachment_type.JSON,
                )

            # Execute HTTP request
            response = self.session.request(method, url, **kwargs)

            # Log status code
            allure.attach(
                str(response.status_code),
                name="Response Status Code",
                attachment_type=allure.attachment_type.TEXT,
            )

            # Log response body if valid JSON
            try:
                response_body = response.json()
                allure.attach(
                    json.dumps(response_body, indent=2, ensure_ascii=False),
                    name="Response JSON Body",
                    attachment_type=allure.attachment_type.JSON,
                )
            except Exception:
                if response.text:
                    allure.attach(
                        response.text,
                        name="Response Raw Text",
                        attachment_type=allure.attachment_type.TEXT,
                    )

            return response

    def get(self, endpoint: str, **kwargs):
        return self._send_request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs):
        return self._send_request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs):
        return self._send_request("PUT", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        return self._send_request("DELETE", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs):
        return self._send_request("PATCH", endpoint, **kwargs)