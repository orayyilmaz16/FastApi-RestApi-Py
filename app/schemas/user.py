from pydantic import BaseModel,EmailStr

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    bio: str | None
    avatar_url: str | None
    skills: list[str]
    settings: dict
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    email: EmailStr 
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserUpdateSchema(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    bio: str | None = None
    avatar_url: str | None = None
    skills: list[str] | None = None
    settings: dict | None = None


