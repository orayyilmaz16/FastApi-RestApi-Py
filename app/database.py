from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
from app.core.config import settings

# ---------------------------------------------------------
# 1) Engine — Production seviyesinde güçlendirilmiş yapı
# ---------------------------------------------------------

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,                     # Logları kapat (gerekirse True yaparsın)
    pool_pre_ping=True,             # Bağlantı koparsa otomatik yeniler
    poolclass=QueuePool,            # Daha stabil connection pool
    pool_size=10,                   # Aynı anda 10 bağlantı
    max_overflow=20,                # Gerekirse +20 bağlantı daha açar
    connect_args={"check_same_thread": False} 
        if settings.DATABASE_URL.startswith("sqlite")
        else {}
)

# ---------------------------------------------------------
# 2) Session — Otomatik yönetim + güvenli yapı
# ---------------------------------------------------------

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False          # Commit sonrası objeler geçersiz olmaz
)

# ---------------------------------------------------------
# 3) Base — Alembic için metadata kaynağı
# ---------------------------------------------------------

Base = declarative_base()

# ---------------------------------------------------------
# 4) Dependency — Her request için güvenli DB session
# ---------------------------------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()               # Hata olursa rollback
        raise
    finally:
        db.close()                  # Bağlantı mutlaka kapanır
