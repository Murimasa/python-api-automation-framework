
import os
import allure
import requests
from utils.allure_helper import attach_http_exchange

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
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            url = endpoint
        else:
            normalized_endpoint = (
                endpoint if endpoint.startswith("/") else f"/{endpoint}"
            )
            url = f"{self.base_url}{normalized_endpoint}"

        with allure.step(f"HTTP {method.upper()} {endpoint}"):
            response = self.session.request(method=method, url=url, **kwargs)
            attach_http_exchange(response)

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