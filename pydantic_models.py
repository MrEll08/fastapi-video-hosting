from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import Optional


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


class VideoCreate(BaseModel):
    title: str = Field(..., description="Video title")
    description: str = Field(description="Video description")


class SubscriptionCreate(BaseModel):
    follower_id: int = Field(..., description="Follower ID")
    followed_id: int = Field(..., description="Followed ID")

    @model_validator(mode="before")
    def validate(cls, values):
        if values.get("follower_id") == values.get("followed_id"):
            raise ValueError("Follower and Followed IDs can't be same")
        return values
