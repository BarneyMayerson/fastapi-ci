from sqlalchemy import Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    cooking_time: Mapped[int] = mapped_column(Integer, nullable=False)
    ingredients: Mapped[JSON] = mapped_column(JSON)
    views: Mapped[int] = mapped_column(Integer, default=0)
