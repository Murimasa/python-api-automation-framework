import allure
import pytest
from core.data_generator import DataGenerator
from core.schemas import PostPatchSchema


@allure.feature("Posts Management")
@allure.story("Read Posts")
def test_get_all_posts(api_client):
    """Verify retrieving list of all posts."""
    response = api_client.get("/posts")

    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list)
    assert len(posts) > 0


@allure.feature("Posts Management")
@allure.story("Create Post")
def test_create_post_with_session(api_client):
    """Verify creating a new post and validating contract schema."""
    payload = DataGenerator.generate_post_data()

    response = api_client.post("/posts", json=payload)

    assert response.status_code == 201
    post = PostPatchSchema.model_validate(response.json())
    assert post.title == payload["title"]
    assert post.user_id == payload["userId"]
    assert isinstance(post.id, int)