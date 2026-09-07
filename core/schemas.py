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