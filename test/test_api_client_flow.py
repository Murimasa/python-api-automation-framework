import allure


@allure.epic("Core Platform API")
@allure.feature("Automated CRUD Flow via ApiClient")
class TestClientFlow:

    def test_get_post(self, custom_api):
        response = custom_api.get("/posts/1")
        assert response.status_code == 200
        assert response.json()["id"] == 1

    def test_create_post(self, custom_api):
        payload = {
            "title": "Clean Architecture",
            "body": "ApiClient handles logging automatically",
            "userId": 1,
        }
        response = custom_api.post("/posts", json=payload)
        assert response.status_code == 201
        assert response.json()["title"] == payload["title"]

    def test_update_post(self, custom_api):
        payload = {
            "id": 1,
            "title": "Updated Title",
            "body": "Updated Body",
            "userId": 1,
        }
        response = custom_api.put("/posts/1", json=payload)
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Title"

    def test_delete_post(self, custom_api):
        response = custom_api.delete("/posts/1")
        assert response.status_code == 200