from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List


# Base
class BaseConfig:
    model_config = {
        "from_attributes": True  # Cách mới
    }


class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: str


class Signup(BaseModel):
    full_name: str
    email: str
    password: str

    class Config(BaseConfig):
        pass


class UserOut(BaseModel):
    message: str
    data: UserBase

    class Config(BaseConfig):
        pass


# Token
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'
    expires_in: int
    

class LoginForm(BaseModel):
    email: str
    password: str
    # otp_code: str | None = None  # Thêm mã OTP nếu có
    # remember_me: bool = False