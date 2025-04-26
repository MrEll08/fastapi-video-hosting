from pydantic import BaseModel, ConfigDict, Field, model_validator, computed_field
from typing import Optional
from constants import GET_VIDEO_PATH


class UserCreate(BaseModel):
    login: str = Field(..., description="User's login")
    nickname: str = Field(..., description="User's nickname")
    password: str = Field(..., min_length=1)


class UserLogin(BaseModel):
    login: str
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    login: str
    nickname: str


class AuthorSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes = True
    )

    id: int = Field(..., description="Author's ID")
    nickname: str = Field(..., description="Author's nickname")



class VideoFeedSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes = True
    )

    id: int = Field(..., description="Video ID")
    title: str = Field(..., description="Video title")
    author_id: int = Field(..., description="Video author's id")
    filename: str = Field(..., description="Video path")

    author: AuthorSchema

    @computed_field(return_type=str)
    @property
    def path(self):
        return f"{GET_VIDEO_PATH}/{self.filename}"


class VideoSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes = True
    )

    id: int = Field(..., description="Video ID")
    title: str = Field(..., description="Video title")
    description: str = Field(description="Video description")
    filename: str = Field(..., description="Video path on server")
    likes: int = Field(default=0, description="Video likes")
    dislikes: int = Field(default=0, description="Video likes")

    author: AuthorSchema

    @computed_field(return_type=str)
    @property
    def path(self):
        return f"{GET_VIDEO_PATH}/{self.filename}"


class SubscriptionCreate(BaseModel):
    follower_id: int = Field(..., description="Follower ID")
    followed_id: int = Field(..., description="Followed ID")

    @model_validator(mode="before")
    def validate(cls, values):
        if values.get("follower_id") == values.get("followed_id"):
            raise ValueError("Follower and Followed IDs can't be same")
        return values
