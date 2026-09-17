import allure

from core.data_generator import DataGenerator
from core.schemas import PostPatchSchema


@allure.epic("Core Platform API")
@allure.feature("Resource Lifecycle")
class TestPostLifecycle:

    def test_update_existing_post(self, api_client, created_post):
        """Verify updating an existing resource via PUT request."""
        update_payload = DataGenerator.generate_post_data()

        # Mock API does not persist new IDs in memory, so we target stable ID 1
        target_id = 1

        response = api_client.put(f"/posts/{target_id}", json=update_payload)
        assert response.status_code == 200

        updated_post = PostPatchSchema.model_validate(response.json())
        assert updated_post.title == update_payload["title"]
        assert updated_post.body == update_payload["body"]

    def test_read_existing_post(self, api_client, created_post):
        """Attempt reading an entity created during setup phase."""
        post_id = created_post["id"]

        response = api_client.get(f"/posts/{post_id}")
        # Mock API does not persist records physically, so 404 is expected
        assert response.status_code == 404