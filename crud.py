from sqlalchemy.orm import Session
from models import Recipe
from schemas import RecipeCreate


def create_recipe(db: Session, recipe: RecipeCreate):
    db_recipe = Recipe(**recipe.model_dump(), views=0)

    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)

    return db_recipe
