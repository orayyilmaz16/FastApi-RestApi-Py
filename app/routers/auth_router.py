from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import LoginSchema
from app.services.user_service import create_user, authenticate_user
from app.auth.jwt_handler import create_access_token
from app.auth.jwt_current_user import get_current_user
from app.auth.token_service import create_refresh_token, verify_refresh_token
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])


# -------------------------
# GET /auth/me
# -------------------------
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


# -------------------------
# POST /auth/register
# -------------------------
@router.post("/register", response_model=UserResponse)
def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user_data = UserCreate(username=username, email=email, password=password)
    new_user = create_user(db, user_data)
    return new_user


# -------------------------
# POST /auth/token
# -------------------------
@router.post("/token")
def login(form_data: LoginSchema, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token(db, user.id)  # 🔥 EKLENDİ

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,   # 🔥 EKLENDİ
        "token_type": "bearer"
    }


# -------------------------
# POST /auth/refresh
# -------------------------
@router.post("/refresh")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    token_data = verify_refresh_token(db, refresh_token)

    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access = create_access_token({"sub": str(token_data.user_id)})

    return {
        "access_token": new_access,
        "token_type": "bearer"
    }


# -------------------------
# POST /auth/logout
# -------------------------
@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_db)):
    token_data = verify_refresh_token(db, refresh_token)

    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    db.delete(token_data)
    db.commit()

    return {"message": "Logged out successfully"}
