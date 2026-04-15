from datetime import datetime, timedelta
from jose import jwt
from app.models.refresh_token import RefreshToken
from app.database import get_db
from sqlalchemy.orm import Session
import secrets

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_minutes=15):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(db: Session, user_id: int):
    token = secrets.token_hex(32)
    expires = datetime.utcnow() + timedelta(days=7)

    db_token = RefreshToken(
        user_id=user_id,
        token=token,
        expires_at=expires
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return token

def verify_refresh_token(db: Session, token: str):
    db_token = db.query(RefreshToken).filter(RefreshToken.token == token).first()
    if not db_token:
        return None
    if db_token.expires_at < datetime.utcnow():
        return None
    return db_token
