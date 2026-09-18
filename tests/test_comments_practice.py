import allure
import pytest

from core.schemas import CommentSchema


@allure.feature("Comments Management")
@allure.story("Read Single Comment")
def test_get_single_comment(api_client):
    """Retrieve existing comment and validate contract via Pydantic."""
    response = api_client.get("/comments/1")
    assert response.status_code == 200

    comment = CommentSchema.model_validate(response.json())
    assert comment.id == 1
    assert comment.post_id == 1


@allure.feature("Comments Management")
@allure.story("Create Comment")
def test_create_comment(api_client):
    """Create comment and verify response contract and fields."""
    payload = {
        "postId": 1,
        "name": "alex_tester",
        "email": "alex@example.com",
        "body": "Bodusmady",
    }
    response = api_client.post("/comments", json=payload)
    assert response.status_code == 201

    created_comment = CommentSchema.model_validate(response.json())
    assert created_comment.name == payload["name"]
    assert created_comment.email == payload["email"]
    assert isinstance(created_comment.id, int)


@allure.feature("Comments Management")
@allure.story("Negative ID Scenarios")
@pytest.mark.parametrize(
    "invalid_id, expected_status",
    [
        pytest.param(0, 404, id="zero_id"),
        pytest.param(501, 404, id="out_of_range_id"),
    ],
)
def test_get_invalid_comment_id(api_client, invalid_id, expected_status):
    """Ensure non-existent comment IDs return proper error status codes."""
    response = api_client.get(f"/comments/{invalid_id}")
    assert response.status_code == expected_status