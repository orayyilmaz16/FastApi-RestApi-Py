from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from app.database import Base, engine
from app.core.config import settings

# ---------------------------------------------------------
# Alembic Config
# ---------------------------------------------------------
config = context.config

# Eğer alembic.ini içinde sqlalchemy.url boşsa,
# settings.DATABASE_URL otomatik olarak kullanılır.
if config.get_main_option("sqlalchemy.url") in ("", None):
    config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Modellerin metadata’sı
target_metadata = Base.metadata


# ---------------------------------------------------------
# Offline Migration
# ---------------------------------------------------------
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,          # Kolon tipi değişikliklerini algılar
        compare_server_default=True # Varsayılan değer değişikliklerini algılar
    )

    with context.begin_transaction():
        context.run_migrations()


# ---------------------------------------------------------
# Online Migration
# ---------------------------------------------------------
def run_migrations_online() -> None:
    connectable = engine  # FastAPI’nin engine’i kullanılıyor

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            render_as_batch=True      # SQLite için zorunlu (ALTER TABLE desteği yok)
        )

        with context.begin_transaction():
            context.run_migrations()


# ---------------------------------------------------------
# Çalıştır
# ---------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
