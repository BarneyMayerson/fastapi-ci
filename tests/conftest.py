from typing import Generator, Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from database import Base
from main import app, get_db


@pytest.fixture(scope="session")
def engine() -> Generator[Engine, None, None]:
    """Фикстура для создания Engine (один раз на все тесты)"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(engine: Engine) -> Generator[Session, None, None]:
    """Фикстура для изолированной сессии БД (откат после теста)"""
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    # Монки-патч FastAPI зависимости
    app.dependency_overrides[get_db] = lambda: session

    yield session

    # Cleanup
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session: Session) -> Any:
    """Фикстура для TestClient с подменённой БД"""
    yield TestClient(app)
