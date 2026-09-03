import pytest
import requests
from pydantic import BaseModel, EmailStr
from typing import List



# 1. Описываем контракт пользователя через Pydantic-модель
class CommentModel(BaseModel):
    postId:int
    id:int
    name:str
    email:str
    body:str

def test_get_single_comment(base_url, api_client):
    response = api_client.get(f"{base_url}/comments/1")
    assert response.status_code == 200

    user_data =CommentModel.model_validate(response.json())
    assert user_data.id == 1
    assert "@" in user_data.email



def test_create_comment(base_url, api_client):
    payload = {
        "postId": 1,
        "name": "alex_tester",
        "email": "alex@example.com",
        "body":"Bodusmady"
    }
    response = api_client.post(f"{base_url}/comments", json=payload)
    assert response.status_code == 201

    created_data = response.json()
    assert created_data["name"] == payload["name"]
    assert "id" in created_data

@pytest.mark.parametrize("invalid_id, expected_status",[
    (0, 404),
    (501, 404)
])
def test_get_multiple_users(base_url,invalid_id, expected_status):
    response = requests.get(f"{base_url}/comments/{invalid_id}")
    assert response.status_code == expected_status
