
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    totp_secret: str
    is_verified: bool

    class Config:
        orm_mode = True

