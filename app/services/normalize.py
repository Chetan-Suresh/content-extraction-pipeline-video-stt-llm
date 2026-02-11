from app.models import Ingredient, Step, Recipe

def normalize_recipe(raw: dict) -> Recipe:
    ingredients = [Ingredient(name=i, quantity=None) for i in raw["ingredients"]]
    steps = [Step(instruction=s) for s in raw["steps"]]

    return Recipe(
        title=raw["title"],
        ingredients=ingredients,
        steps=steps
    )
