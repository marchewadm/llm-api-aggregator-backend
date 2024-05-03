from pydantic import BaseModel


class ApiKeyBase(BaseModel):
    key: str


class ApiKeyCreate(ApiKeyBase):
    pass


class ApiKey(ApiKeyBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    name: str
    password: str
    password2: str


class User(UserBase):
    id: int
    api_keys: list[ApiKey] = []

    class Config:
        orm_mode = True
