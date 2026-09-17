from pydantic import BaseModel, EmailStr, Field


class CommentSchema(BaseModel):
    post_id: int = Field(alias="postId")
    id: int
    name: str
    email: EmailStr
    body: str

    model_config = {
        "populate_by_name": True,
        "extra": "ignore",
    }


class PostPatchSchema(BaseModel):
    id: int
    title: str
    body: str | None = None
    user_id: int = Field(alias="userId")

    model_config = {
        "populate_by_name": True,
    }

class GeoSchema(BaseModel):
    lat: str
    lng: str


class AddressSchema(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: GeoSchema


class CompanySchema(BaseModel):
    name: str
    catch_phrase: str = Field(alias="catchPhrase")
    bs: str

    model_config = {
        "populate_by_name": True,
    }


class UserSchema(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    address: AddressSchema
    phone: str
    website: str
    company: CompanySchema