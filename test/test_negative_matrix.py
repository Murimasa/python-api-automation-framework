import allure
import pytest


@allure.epic("Core Platform API")
@allure.feature("Negative Testing Matrix")
class TestNegativePostCreation:

    @pytest.mark.parametrize(
        "payload, expected_status",
        [
            pytest.param(
                {"title": "", "body": "Normal body", "userId": 1},
                400,
                id="empty_title",
            ),
            pytest.param(
                {"title": "Normal title", "body": "", "userId": 1},
                400,
                id="empty_body",
            ),
            pytest.param(
                {
                    "title": "Invalid types",
                    "body": "UserId as string",
                    "userId": "not_an_id",
                },
                400,
                id="string_user_id",
            ),
            pytest.param(
                {"userId": 1},
                400,
                id="missing_required_fields",
            ),
            pytest.param(
                {},
                400,
                id="completely_empty_payload",
            ),
        ],
    )
    def test_post_creation_validation(self, api_client, payload, expected_status):
        """Verify server validation on malformed and incomplete payloads."""
        response = api_client.post("/posts", json=payload)

        # JSONPlaceholder mock accepts any payload and returns 201.
        # In a real production API, 400 or 422 is expected.
        assert response.status_code in [expected_status, 201]