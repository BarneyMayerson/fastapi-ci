import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from module_30_ci_linters.homework.main import app, get_db
from module_30_ci_linters.homework.database import Base


@pytest.fixture(scope="session")
def engine():
    """Фикстура для создания Engine (один раз на все тесты)"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(engine):
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
def client(db_session):
    """Фикстура для TestClient с подменённой БД"""
    yield TestClient(app)
