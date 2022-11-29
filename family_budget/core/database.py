from collections import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from family_budget.core.config import get_settings

settings = get_settings()

engine = create_engine(settings.DB_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
POSTGRES_UTC_NOW = text("(now() at time zone 'utc')")


def get_db_session() -> Generator:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        if db is not None:
            db.close()
