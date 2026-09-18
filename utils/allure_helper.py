import json
import allure
import requests


def response_to_curl(response: requests.Response) -> str:
    """Generate a reproducible cURL command string from a Response object."""
    req = response.request
    parts = [f"curl -X {req.method} '{req.url}'"]

    for header_name, header_value in req.headers.items():
        parts.append(f"-H '{header_name}: {header_value}'")

    if req.body:
        body = req.body
        if isinstance(body, bytes):
            body = body.decode("utf-8", errors="replace")
        parts.append(f"-d '{body}'")

    return " \\\n  ".join(parts)


def attach_http_exchange(response: requests.Response) -> None:
    """Attach cURL command and response payload to the active Allure step/tests."""
    method = response.request.method
    url_path = response.request.path_url
    status_code = response.status_code

    # 1. Attach cURL command
    allure.attach(
        response_to_curl(response),
        name=f"cURL: {method} {url_path}",
        attachment_type=allure.attachment_type.TEXT,
    )

    # 2. Attach response payload
    try:
        data = response.json()
        formatted_json = json.dumps(data, indent=2, ensure_ascii=False)
        allure.attach(
            formatted_json,
            name=f"Response Body [{status_code}]",
            attachment_type=allure.attachment_type.JSON,
        )
    except (ValueError, json.JSONDecodeError):
        allure.attach(
            response.text or "<empty response>",
            name=f"Response Text [{status_code}]",
            attachment_type=allure.attachment_type.TEXT,
        )
def _send_request(
    self,
    method: str,
    path: str,
    timeout: tuple[float, float] | None = None,
    **kwargs,
) -> requests.Response:
    url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
    current_timeout = timeout or getattr(
        self, "default_timeout", getattr(self, "timeout", (3.05, 10))
    )

    # Wrap the entire network interaction into a named Allure step
    with allure.step(f"HTTP {method.upper()} {path}"):
        response = self.session.request(
            method=method, url=url, timeout=current_timeout, **kwargs
        )
        attach_http_exchange(response)

    return response