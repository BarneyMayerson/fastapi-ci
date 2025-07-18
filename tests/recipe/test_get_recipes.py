from typing import Any

from fastapi import status
from sqlalchemy.orm import Session

from models import Recipe


def test_it_can_get_recipes_sorted_by_views_and_cooking_time(client: Any, db_session: Session) -> None:
    # Тестовые данные
    recipes_data = [
        {"title": "Рецепт 1", "cooking_time": 20, "views": 100, "ingredients": ["a"]},
        {"title": "Рецепт 2", "cooking_time": 10, "views": 100, "ingredients": ["b"]},
        {"title": "Рецепт 3", "cooking_time": 30, "views": 50, "ingredients": ["c"]},
    ]

    for recipe_data in recipes_data:
        db_recipe = Recipe(**recipe_data)
        db_session.add(db_recipe)
    db_session.commit()

    # Отправка GET-запроса
    response = client.get("/recipes/")

    # Проверка ответа
    assert response.status_code == status.HTTP_200_OK
    recipes = response.json()

    # Проверяем сортировку: сначала по views (убывание), затем по cooking_time (возрастание)
    assert recipes[0]["title"] == "Рецепт 2"  # views=100, cooking_time=10
    assert recipes[1]["title"] == "Рецепт 1"  # views=100, cooking_time=20
    assert recipes[2]["title"] == "Рецепт 3"  # views=50, cooking_time=30
