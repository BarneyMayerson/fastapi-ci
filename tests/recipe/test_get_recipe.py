from fastapi import status
from module_30_ci_linters.homework.models import Recipe


def test_get_recipe_by_id(client, db_session):
    # Тестовый рецепт
    recipe_data = {
        "title": "Паста Карбонара",
        "cooking_time": 30,
        "ingredients": ["спагетти", "яйца", "бекон"],
        "views": 0,
    }
    db_recipe = Recipe(**recipe_data)
    db_session.add(db_recipe)
    db_session.commit()

    # Отправляем запрос
    response = client.get(f"/recipes/{db_recipe.id}")

    # Проверяем ответ
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == recipe_data["title"]
    assert data["cooking_time"] == recipe_data["cooking_time"]
    assert data["ingredients"] == recipe_data["ingredients"]
    assert len(data["ingredients"]) == 3
    assert data["views"] == 1  # Проверяем, что счетчик views увеличился на 1


def test_get_nonexistent_recipe(client):
    # Пытаемся получить несуществующий рецепт
    response = client.get("/recipes/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
