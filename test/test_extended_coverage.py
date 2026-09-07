import allure
from core.schemas import CommentSchema, PostPatchSchema


@allure.epic("core REST Operations")
@allure.feature("Extended API Scenarios")
class TestExtendedAPI:

    @allure.story("Query Filtering")
    @allure.severity(allure.severity_level.NORMAL)
    def test_filter_comments_by_post_id(self, api_client):
        """Verify filtering comments using query parameters."""
        target_post_id = 2

        with allure.step(f"Fetch comments for postId={target_post_id} via query params"):
            response = api_client.get("/comments", params={"postId": target_post_id})

        with allure.step("Validate response code and payload size"):
            assert response.status_code == 200
            comments = response.json()
            assert len(comments) > 0, "Comments list should not be empty"

        with allure.step("Enforce schema and data integrity across all items"):
            for item in comments:
                validated_comment = CommentSchema.model_validate(item)
                assert validated_comment.post_id == target_post_id

    @allure.story("Nested Resources")
    @allure.severity(allure.severity_level.NORMAL)
    def test_nested_post_comments(self, api_client):
        """Verify accessing nested relational route /posts/{id}/comments."""
        post_id = 1

        with allure.step(f"Request nested comments for post {post_id}"):
            response = api_client.get(f"/posts/{post_id}/comments")

        with allure.step("Validate response status and contract"):
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            assert len(data) > 0

            # Validate first element schema
            CommentSchema.model_validate(data[0])

    @allure.story("Partial Updates")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_patch_existing_post(self, api_client):
        """Verify partial update via PATCH modifies only the specified fields."""
        post_id = 1
        payload = {"title": "Partially Patched Title via Automation"}

        with allure.step(f"Execute PATCH on /posts/{post_id}"):
            response = api_client.patch(f"/posts/{post_id}", json=payload)

        with allure.step("Validate response code"):
            assert response.status_code == 200

        with allure.step("Validate mutated field while preserving entity structure"):
            data = response.json()
            assert data["title"] == payload["title"]
            # Contract assertion
            PostPatchSchema.model_validate(data)

    @allure.story("Resource Deletion")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_resource(self, api_client):
        """Verify standard deletion response."""
        post_id = 1

        with allure.step(f"Send DELETE request for /posts/{post_id}"):
            response = api_client.delete(f"/posts/{post_id}")

        with allure.step("Assert deletion status code"):
            assert response.status_code in (200, 204)