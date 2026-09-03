# Фиктивные данные, будто мы получили их из API бэкенда
response_data = {
    "status_code": 200,
    "user_id": 42,
    "username": "tester_pro",
    "roles": ["tester", "qa_lead", "admin"],
    "is_active": True
}


def test_status_code_is_200():
    """Проверяем, что сервер вернул статус 200"""
    assert response_data["status_code"] == 200


def test_user_has_tester_role():
    """Проверяем наличие роли tester"""
    assert "tester" in response_data["roles"]


def test_user_is_active():
    """Проверяем, что пользователь активен"""
    assert response_data["is_active"] is True