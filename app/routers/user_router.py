from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate,UserResponse
from app.services.user_service import create_user,get_users
from app.auth.jwt_current_user import get_current_user
from app.models.user import User

router = APIRouter(prefix="/users",tags=["Users"])

@router.post("/",response_model=UserResponse)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.get("/",response_model=list[UserResponse])
def get_users_endpoint(db: Session = Depends(get_db)):
    return get_users(db)

