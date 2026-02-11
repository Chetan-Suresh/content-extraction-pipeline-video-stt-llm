from pydantic import BaseModel
from typing import List, Optional

class Ingredient(BaseModel):
    name: str
    quantity: Optional[str] = None

class Step(BaseModel):
    instruction: str

class Recipe(BaseModel):
    title: str
    ingredients: List[Ingredient]
    steps: List[Step]
