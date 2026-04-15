from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.sqlite import JSON
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    bio = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)

    skills = Column(JSON, default=[])      # 🔥 yetkinlikler
    settings = Column(JSON, default={})    # 🔥 kullanıcı ayarları

    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
