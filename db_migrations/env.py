import sys
from pathlib import Path
from importlib import import_module
import logging
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from modularapi.settings import get_setting

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support


p = Path("modules")
if not p.is_dir():
    logging.error("There is no modules directory !")
    exit(1)

sys.path.append(str(p.resolve()))

for module in Path("modules").glob("*"):
    # ensure the module is a directory and not a file.
    if module.is_dir():
        # check if <module_name>/db.py exists
        if (module / "db.py").is_file():
            module_name = ".".join(module.parts[1:] + ("db",))
            import_module(module_name)


# from module_a.db import User
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# print(Path().resolve())
# import os
# print(os.getcwd())
from modularapi.db import db  # noqa: 402

target_metadata = db

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

config.set_main_option("sqlalchemy.url", get_setting().PG_DNS)


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
