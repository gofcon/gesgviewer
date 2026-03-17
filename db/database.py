"""
SQLAlchemy 엔진 / 세션 팩토리
"""
import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config.settings import DB_URL, DB_PATH


class Base(DeclarativeBase):
    pass


# data 디렉토리 자동 생성
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

engine = create_engine(
    DB_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

# SQLite 외래키 활성화
@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_connection, _):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class _SessionContext:
    """with get_session() as session: 패턴 지원"""
    def __init__(self):
        self._session = SessionLocal()

    def __enter__(self):
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self._session.rollback()
        self._session.close()
        return False


def get_session() -> _SessionContext:
    """
    with get_session() as session:
        ...
    """
    return _SessionContext()
