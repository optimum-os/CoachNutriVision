import os
import base64
import requests
from openai import OpenAI
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API Key from the environment variable
api_key = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI client
client = OpenAI(
    api_key=api_key
)

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Documentation: https://platform.openai.com/docs/guides/vision
# Function to detect ingredients from the image
def detect_ingredients_from_image(image_path):
    # Encode the image
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What’s in this image?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_json = response.json()
    print(response_json)
    ingredients = response_json['choices'][0]['message']['content']
    return ingredients

# Function to generate a recipe based on the detected ingredients and prompt
def generate_recipe(ingredients, prompt):
    full_prompt = f"Here are the ingredients: {ingredients}. {prompt}"

    model = "gpt-3.5-turbo-0125" # gpt-4o
    response = client.chat.completions.create(model=model,  messages=[{"role": "system", "content": full_prompt}], max_tokens=500)
    print(response)
    recipe = response.choices[0].message.content
    return recipe

# Main function
def main(image_path, prompt):
    ingredients = detect_ingredients_from_image(image_path)
    print("Identified ingredients:", ingredients)

    recipe = generate_recipe(ingredients, prompt)
    print("Generated recipe:", recipe)

# Example usage
image_path = "images/ingredients/01.jfif"
prompt = """
    Suggest a list of recipe list using these ingredients.
    for each recipe, provide the following details:
    1) List the ingredients needed for the recipe
    2) Detailed list of process to make the recipe
    3) Time required to make the recipe
    4) Nutritional value of the recipe
"""
main(image_path, prompt)
