from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.jwt_current_user import get_current_user
from app.schemas.user import UserUpdateSchema, UserResponse
from app.services.user_service import update_user_profile, get_all_users

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
def get_me(current_user = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
def update_me(
    data: UserUpdateSchema,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return update_user_profile(db, current_user.id, data)

@router.get("/", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(403, "Admin required")

    return get_all_users(db)
