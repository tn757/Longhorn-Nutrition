from google import genai
from google.genai import types # <-- Import the 'types' module
from dotenv import load_dotenv
import json
import os


def remove_triple_backticks(s: str) -> str:
    lines = s.splitlines()
    if lines:
        if lines[0].strip() == "```json":
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
    return "\n".join(lines)


# Load environment variables from .env
load_dotenv()

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

prompt = "You are an AI nutritionist. Attached below are three jsons. The first json details the daily recommended value of each nutrient. The second json details a menu of foods, as well as their nutritional values. Generate 5 mealplans, (breakfast, lunch dinner), emphasizing tastiness as well as nutritional value. The total nutrients of each meal plan should be close to or better than the recommended daily values of nutrients. Finally, I have attached an example of how you should return your output. You should respond with only a json format of each of the meals. Do not start or end the file with markdown ticks, start immediately with the json."
with open('./app/public/dv.json', 'r') as f:
    dv_targets = f.read()
with open('./app/public/menu.json', 'r') as f:
    menu = f.read()
with open('./app/public/example.json', 'r') as f:
    example = f.read()

prompt = prompt + "\n" + dv_targets + "\n" + menu + "\n" + example

# Create a configuration object to hold the temperature setting
config = types.GenerateContentConfig(
    temperature=0
)

# Pass the configuration object to the 'config' parameter
response = client.models.generate_content(
    model="gemini-2.5-pro", 
    contents=prompt,
    config=config, 
)

meals = response.text
meals = remove_triple_backticks(meals)

print(meals)

with open('./app/public/meals.json', 'w') as f:
    f.write(meals)