import os
from typing import Any, Generator

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, init_db

if not os.path.exists("recipes.db"):
    init_db()

app = FastAPI(
    title="Кулинарная книга",
    description="API для управления рецептами с возможностью просмотра, добавления и сортировки рецептов",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Рецепты",
            "description": "Операции с рецептами - создание, просмотр, сортировка",
        }
    ],
)


# Зависимость для получения сессии БД
def get_db() -> Generator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/recipes/", response_model=list[schemas.Recipe], tags=["Рецепты"])
def get_recipes(db: Session = Depends(get_db)) -> list[schemas.Recipe]:
    """Возвращает список рецептов, отсортированный по популярности (views) и времени готовки."""
    recipes = (
        db.query(models.Recipe)
        .order_by(
            desc(models.Recipe.views),  # Сначала сортируем по views (убывание)
            asc(models.Recipe.cooking_time),  # Затем по cooking_time (возрастание)
        )
        .all()
    )
    return [schemas.Recipe.model_validate(recipe) for recipe in recipes]


@app.get("/recipes/{recipe_id}", response_model=schemas.Recipe, tags=["Рецепты"])
def get_recipe(recipe_id: int, db: Session = Depends(get_db)) -> type[schemas.Recipe]:
    """
    Возвращает детальную информацию о рецепте по его ID.
    При каждом запросе увеличивает счётчик просмотров (views) на 1.
    """
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()

    if not db_recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")

    db_recipe.views += 1
    db.commit()
    db.refresh(db_recipe)

    return db_recipe


@app.post("/recipes/", response_model=schemas.Recipe, tags=["Рецепты"])
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)) -> schemas.Recipe:
    """Создаёт новый рецепт."""
    return crud.create_recipe(db=db, recipe=recipe)
