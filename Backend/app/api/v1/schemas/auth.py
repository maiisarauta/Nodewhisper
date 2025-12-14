from pydantic import BaseModel, EmailStr

class RegisterUser(BaseModel):
    email: EmailStr
    username: str
    password: str

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
