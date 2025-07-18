import pytest
from fastapi import status

from module_30_ci_linters.homework.models import Recipe


@pytest.mark.parametrize(
    "data, expected_status",
    [
        # Успешные случаи
        (
            {"title": "Паста", "cooking_time": 10, "ingredients": ["тест"]},
            status.HTTP_200_OK,
        ),
        # Ошибки валидации
        (
            {"title": "", "cooking_time": 10, "ingredients": ["тест"]},  # Пустой title
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        (
            {
                "title": "A" * 101,
                "cooking_time": 10,
                "ingredients": ["тест"],
            },  # Слишком длинный title
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        (
            {
                "title": "Паста",
                "cooking_time": 0,
                "ingredients": ["тест"],
            },  # cooking_time <= 0
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        (
            {
                "title": "Паста",
                "cooking_time": 2000,
                "ingredients": ["тест"],
            },  # cooking_time > 1440 мин.
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        (
            {
                "title": "Паста",
                "cooking_time": 10,
                "ingredients": [],
            },  # Нет ингредиентов
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        (
            {
                "title": "Паста",
                "cooking_time": 10,
                "ingredients": ["  "],
            },  # Пустой ингредиент
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
    ],
)
def test_recipe_validation(client, data, expected_status):
    response = client.post("/recipes/", json=data)
    assert response.status_code == expected_status


def test_it_can_create_a_recipe(client, db_session):
    recipe_data = {
        "title": "Паста Карбонара",
        "cooking_time": 30,
        "ingredients": ["спагетти", "яйца", "бекон", "пармезан"],
    }

    response = client.post("/recipes/", json=recipe_data)

    assert response.status_code == 200
    assert response.json()["title"] == "Паста Карбонара"
    assert response.json()["cooking_time"] == 30
    assert "ingredients" in response.json()

    db_recipe = (
        db_session.query(Recipe).filter(Recipe.id == response.json()["id"]).first()
    )

    assert db_recipe is not None, "Запись не найдена в базе данных"
    assert db_recipe.title == recipe_data["title"]
    assert db_recipe.cooking_time == recipe_data["cooking_time"]
    assert db_recipe.ingredients == recipe_data["ingredients"]
    assert db_recipe.views == 0
