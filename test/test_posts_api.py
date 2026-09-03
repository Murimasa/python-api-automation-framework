def test_get_all_posts(base_url, api_client):
    """Тест списка постов: фикстуры подтянулись из conftest.py без импорта!"""
    response = api_client.get(f"{base_url}/posts")

    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list)  # проверяем, что вернулся именно список
    assert len(posts) > 0  # проверяем, что список не пустой


def test_create_post_with_session(base_url, api_client):
    """Создание нового поста через общую сессию"""
    new_post = {
        "title": "My first auto test post",
        "body": "Running automated tests with Pytest and requests",
        "userId": 1
    }

    response = api_client.post(f"{base_url}/posts", json=new_post)

    assert response.status_code == 201
    created_data = response.json()
    assert created_data["title"] == new_post["title"]
    assert "id" in created_data