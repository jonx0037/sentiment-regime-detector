"""Database type helpers for cross-dialect compatibility."""

from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import JSON, TypeDecorator


class JSONBCompat(TypeDecorator):
    """Behaves like PostgreSQL JSONB but compiles on SQLite for tests."""

    impl = JSONB
    cache_ok = True

    def __init__(self) -> None:  # pragma: no cover - simple wiring
        super().__init__()
        self._pg_impl = JSONB(astext_type=Text())

    def load_dialect_impl(self, dialect):  # type: ignore[override]
        if dialect.name == "sqlite":
            return dialect.type_descriptor(JSON())
        return dialect.type_descriptor(self._pg_impl)
