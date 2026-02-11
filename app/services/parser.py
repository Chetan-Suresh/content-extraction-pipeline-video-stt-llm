import os
import json
from groq import Groq
from dotenv import load_dotenv
from app.models import Recipe, Ingredient, Step

# Load environment variables from .env file
load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

def parse_recipe(transcript: str) -> Recipe:
    """
    Sends the raw transcript to Groq Llama 3 to extract structured JSON.
    """
    prompt = f"""
    You are an expert chef. Extract a structured recipe from the following video transcript.
    Ignore conversational filler. 
    
    TRANSCRIPT:
    {transcript}
    
    OUTPUT FORMAT (JSON ONLY):
    {{
      "title": "Recipe Title",
      "ingredients": [
        {{"name": "Item name", "quantity": "Quantity (e.g. 2 cups, 100g)"}}
      ],
      "steps": [
        {{"instruction": "Clear, concise step."}}
      ]
    }}
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a JSON-only API. Output strictly JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )

        # Parse JSON response
        result_text = completion.choices[0].message.content
        data = json.loads(result_text)

        # Convert to Pydantic models
        ingredients = [Ingredient(name=i["name"], quantity=i.get("quantity")) for i in data.get("ingredients", [])]
        steps = [Step(instruction=s["instruction"]) for s in data.get("steps", [])]

        return Recipe(
            title=data.get("title", "AI Extracted Recipe"),
            ingredients=ingredients,
            steps=steps
        )

    except Exception as e:
        print(f"Groq API Error: {e}")
        # Fallback to empty recipe if AI fails
        return Recipe(title="Error Parsing Recipe", ingredients=[], steps=[])
