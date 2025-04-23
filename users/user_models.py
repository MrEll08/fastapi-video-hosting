from pydantic import BaseModel, ConfigDict, Field


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
