from logging.config import fileConfig
from alembic import context
from sqlalchemy import pool
from sqlalchemy import engine_from_config

from app.db.base import Base
from app.core.config import settings

from app.models import user, wallet, case

config = context.config

config.set_main_option("sqlalchemy.url", settings.DATABASE_URL_SYNC)

if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    """Offline migrations."""
    context.configure(
        url=settings.DATABASE_URL_SYNC,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Online migrations (sync engine)."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.DATABASE_URL_SYNC
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        connect_args={"sslmode": "require"},
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
