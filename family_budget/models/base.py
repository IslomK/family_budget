from typing import cast
import uuid

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from family_budget.core.database import POSTGRES_UTC_NOW

PostgresSQLUUID = cast(
    "sqlalchemy.types.TypeEngine[uuid.UUID]",
    postgresql.UUID(as_uuid=True),
)


@as_declarative()  # type: ignore
class Base:
    __name__: str

    id = Column(PostgresSQLUUID, primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=POSTGRES_UTC_NOW)
    updated_at = Column(DateTime, default=None)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
