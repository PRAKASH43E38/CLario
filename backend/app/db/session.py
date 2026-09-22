import logging
import os
from collections.abc import Generator

from sqlalchemy import inspect, text
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings

logger = logging.getLogger("clario.db")


class Base(DeclarativeBase):
    pass


def get_engine():
    # Use SQLite for tests to avoid needing a running MySQL container during CI/Tests
    if os.environ.get("TESTING") == "True":
        logger.info("Testing mode detected. Using SQLite in-memory database with a shared connection pool.")
        return create_engine(
            "sqlite://",
            poolclass=StaticPool,
            connect_args={"check_same_thread": False},
        )

    try:
        engine = create_engine(settings.database_url, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.exec_driver_sql("SELECT 1")
        logger.info("Connected to MySQL database.")
        return engine
    except Exception as e:
        logger.warning(f"MySQL unavailable ({e}). Falling back to SQLite for development.")
        return create_engine(
            "sqlite://",
            poolclass=StaticPool,
            connect_args={"check_same_thread": False},
        )


engine = get_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def ensure_schema() -> None:
    """Add any newly introduced columns to an existing database without dropping user data."""
    from app.models import learner  # noqa: F401

    inspector = inspect(engine)
    for table in Base.metadata.sorted_tables:
        if not inspector.has_table(table.name):
            continue

        existing_columns = {col["name"] for col in inspector.get_columns(table.name)}
        for column in table.columns:
            if column.name in existing_columns:
                continue

            column_type = column.type.compile(dialect=engine.dialect)
            column_sql = f"{column.name} {column_type}"
            if not column.nullable:
                column_sql += " NOT NULL"
            if column.default is not None and not callable(column.default.arg):
                default_value = column.default.arg
                if isinstance(default_value, str):
                    default_value = repr(default_value)
                column_sql += f" DEFAULT {default_value}"

            with engine.begin() as conn:
                conn.execute(text(f"ALTER TABLE {table.name} ADD COLUMN {column_sql}"))


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables() -> None:
    from app.models import learner  # noqa: F401

    Base.metadata.create_all(bind=engine)
    ensure_schema()
