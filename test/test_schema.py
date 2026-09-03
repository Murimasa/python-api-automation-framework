from pydantic import BaseModel, EmailStr
from typing import List


# 1. Описываем контракт пользователя через Pydantic-модель
class GeoModel(BaseModel):
    lat: str
    lng: str


class AddressModel(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: GeoModel


class CompanyModel(BaseModel):
    name: str
    catchPhrase: str
    bs: str


class UserModel(BaseModel):
    id: int
    name: str
    username: str
    email: str
    address: AddressModel
    phone: str
    website: str
    company: CompanyModel


# 2. Сам тест
def test_user_schema_contract(base_url, api_client):
    """Проверка, что сервер возвращает строго правильные типы данных и все поля"""
    response = api_client.get(f"{base_url}/users/1")
    assert response.status_code == 200

    # Пробуем распарсить ответ через модель Pydantic
    # Если хоть одно поле отсутствует или его тип не int/str — тест упадет с ошибкой валидации
    user_data = UserModel.model_validate(response.json())

    # Дополнительно можно обращаться к полям через точку, а не по ключам словаря:
    assert user_data.id == 1
    assert "@" in user_data.email
