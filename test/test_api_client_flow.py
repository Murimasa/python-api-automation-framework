import allure

from core.data_generator import DataGenerator
from core.schemas import PostPatchSchema


@allure.epic("Core Platform API")
@allure.feature("Automated CRUD Flow via ApiClient")
class TestClientFlow:

    @allure.story("Complete Post CRUD Lifecycle")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_complete_post_crud_flow(self, api_client):
        """Execute sequential end-to-end CRUD flow for post resource."""
        # 1. CREATE
        payload = DataGenerator.generate_post_data()
        create_res = api_client.post("/posts", json=payload)
        assert create_res.status_code == 201
        created_post = PostPatchSchema.model_validate(create_res.json())

        # 2. READ (using stable id=1 due to mock persistence limitation)
        read_res = api_client.get("/posts/1")
        assert read_res.status_code == 200

        # 3. UPDATE
        update_payload = DataGenerator.generate_post_data()
        update_res = api_client.put("/posts/1", json=update_payload)
        assert update_res.status_code == 200
        updated_post = PostPatchSchema.model_validate(update_res.json())
        assert updated_post.title == update_payload["title"]

        # 4. DELETE
        delete_res = api_client.delete("/posts/1")
        assert delete_res.status_code == 200