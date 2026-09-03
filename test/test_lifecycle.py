import allure
from Core.data_generator import DataGenerator


@allure.epic("Core Platform API")
@allure.feature("Resource Lifecycle")
class TestPostLifecycle:

    def test_update_existing_post(self, custom_api, created_post):
        """Проверяем PUT-запрос к существующему ресурсу."""
        update_payload = DataGenerator.generate_post_data()

        # JSONPlaceholder не сохраняет id 101 в память, поэтому для PUT берем существующий id 1
        target_id = 1

        with allure.step(f"Обновление поста с ID {target_id}"):
            response = custom_api.put(f"/posts/{target_id}", json=update_payload)
            assert response.status_code == 200

            data = response.json()
            assert data["title"] == update_payload["title"]
            assert data["body"] == update_payload["body"]

    def test_read_existing_post(self, custom_api, created_post):
        """Проверяем чтение сущности, созданной на этапе Setup."""
        post_id = created_post["id"]

        with allure.step(f"Попытка чтения только что созданного поста {post_id}"):
            response = custom_api.get(f"/posts/{post_id}")
            # Мок не сохраняет запись физически, поэтому ожидаем 404
            assert response.status_code == 404