# Author: Ing. Jigson Contreras
# Email: supercontreras-ji@hotmail.com
from __future__ import annotations

import logging
import os
import sys
from logging.config import fileConfig

from alembic import context

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.app_factory import create_app
from backend.models import db
from backend.models.customer import Billing, Consumption, Customer

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")

app = create_app()

config.set_main_option("sqlalchemy.url", app.config["SQLALCHEMY_DATABASE_URI"])

target_metadata = db.metadata


def run_migrations_offline() -> None:
    """Ejecuta las migraciones en modo 'offline'."""

    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecuta las migraciones en modo 'online'."""

    with app.app_context():
        with db.engine.connect() as connection:
            context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)

            with context.begin_transaction():
                context.run_migrations()


def run_migrations() -> None:
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()


run_migrations()
