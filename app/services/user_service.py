from fastapi import HTTPException

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate, LoginRequest, UserUpdateSchema


# 🔥 Artık bcrypt değil, argon2 kullanıyoruz
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

# -----------------------------
# Password Helpers
# -----------------------------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# -----------------------------
# User CRUD
# -----------------------------
from sqlalchemy.exc import IntegrityError

def create_user(db: Session, user: UserCreate):
    try:
        hashed_password = hash_password(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Bu email zaten kayıtlı."
        )
    

def get_users(db: Session):
    return db.query(User).all()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def get_user_by_id(user_id: int):
    db = SessionLocal()
    try:
        return db.query(User).filter(User.id == user_id).first()
    finally:
        db.close()

def update_user_profile(db: Session, user_id: int, data: UserUpdateSchema):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user

def get_all_users(db: Session):
    return db.query(User).all()



