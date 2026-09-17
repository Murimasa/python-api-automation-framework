import allure
import pytest


@allure.feature("Users Management")
@allure.story("Parametrized User Retrieval")
@pytest.mark.parametrize(
    "user_id",
    [
        pytest.param(1, id="user_id_1"),
        pytest.param(2, id="user_id_2"),
        pytest.param(3, id="user_id_3"),
    ],
)
def test_get_multiple_users(api_client, user_id):
    """Retrieve multiple valid users using parameterized IDs."""
    response = api_client.get(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["id"] == user_id


@allure.feature("Users Management")
@allure.story("Negative Boundary Scenarios")
@pytest.mark.parametrize(
    "invalid_id, expected_status",
    [
        pytest.param(0, 404, id="zero_boundary_id"),
        pytest.param(9999, 404, id="out_of_range_id"),
        pytest.param(-1, 404, id="negative_id"),
    ],
)
def test_get_user_invalid_ids(api_client, invalid_id, expected_status):
    """Verify non-existent and edge-case IDs return expected HTTP error codes."""
    response = api_client.get(f"/users/{invalid_id}")

    assert response.status_code == expected_status