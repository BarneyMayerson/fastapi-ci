from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./module_30_ci_linters/homework/recipes.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


def init_db():
    """Функция для создания таблиц в БД"""
    Base.metadata.create_all(bind=engine)
