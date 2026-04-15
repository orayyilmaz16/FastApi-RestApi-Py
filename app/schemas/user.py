from pydantic import BaseModel,EmailStr

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr 
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

