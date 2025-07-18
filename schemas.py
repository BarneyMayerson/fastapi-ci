from pydantic import BaseModel, ConfigDict, Field, field_validator


class RecipeBase(BaseModel):
    title: str
    cooking_time: int
    ingredients: list[str]


class RecipeCreate(RecipeBase):
    title: str = Field(min_length=1, max_length=100)
    cooking_time: int = Field(gt=0, le=1440)  # В минутах (макс 24 часа)
    ingredients: list[str] = Field(min_length=1)

    @field_validator("ingredients")
    def validate_ingredients(cls, value):
        if not all(ingredient.strip() for ingredient in value):
            raise ValueError("Ингредиенты не могут быть пустыми")

        return value


class Recipe(RecipeBase):
    id: int
    views: int
    model_config = ConfigDict(from_attributes=True)
