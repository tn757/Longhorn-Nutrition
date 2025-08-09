from google import genai
from google.genai import types
from dotenv import load_dotenv
import json
import os
import sys

def remove_triple_backticks(s: str) -> str:
    lines = s.splitlines()
    if lines:
        if lines[0].strip() == "```json":
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
    return "\n".join(lines)

def main():
    # Load .env locally, but in GitHub Actions prefer secrets
    load_dotenv()

    # Verify environment variable
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set")
        sys.exit(1)

    client = genai.Client()

    prompt = ("You are an AI nutritionist. Attached below are three jsons. The first json details the daily recommended value of each nutrient. "
              "The second json details a menu of foods, as well as their nutritional values. Generate 5 mealplans, (breakfast, lunch dinner), emphasizing tastiness "
              "as well as nutritional value. The total nutrients of each meal plan should be close to or better than the recommended daily values of nutrients. "
              "Finally, I have attached an example of how you should return your output. You should respond with only a json format of each of the meals. "
              "Do not start or end the file with markdown ticks, start immediately with the json.")

    # Assuming this script runs with working directory at repo root
    paths = {
        "dv": './app/public/dv.json',
        "menu": './app/public/menu.json',
        "example": './app/public/example.json',
    }

    try:
        with open(paths["dv"], 'r') as f:
            dv_targets = f.read()
        with open(paths["menu"], 'r') as f:
            menu = f.read()
        with open(paths["example"], 'r') as f:
            example = f.read()
    except FileNotFoundError as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    prompt_full = prompt + "\n" + dv_targets + "\n" + menu + "\n" + example

    config = types.GenerateContentConfig(temperature=0)

    response = client.models.generate_content(
        model="gemini-2.5-pro", 
        contents=prompt_full,
        config=config, 
    )

    meals = remove_triple_backticks(response.text)

    print(meals)

    output_path = './app/public/meals.json'
    with open(output_path, 'w') as f:
        f.write(meals)

if __name__ == "__main__":
    main()
