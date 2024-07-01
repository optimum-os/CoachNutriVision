import base64
import requests
import openai
from dotenv import load_dotenv
import os

# Documentation: https://platform.openai.com/docs/guides/vision

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API Key from the environment variable
api_key = os.getenv('OPENAI_API_KEY')

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

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

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=full_prompt,
        max_tokens=500
    )

    recipe = response.choices[0].text.strip()
    return recipe

# Main function
def main(image_path, prompt):
    ingredients = detect_ingredients_from_image(image_path)
    print("Identified ingredients:", ingredients)

    recipe = generate_recipe(ingredients, prompt)
    print("Generated recipe:", recipe)

# Example usage
image_path = "images/ingredients/01.jfif"
prompt = "Propose me a recipe using these ingredients."
main(image_path, prompt)
