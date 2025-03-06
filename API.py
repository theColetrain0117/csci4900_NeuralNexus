import google.generativeai as genai # replace with your API
import requests
import random

# I'm using Gemini API (replace with your real key and endpoint)
API_KEY = "API Key"
ENDPOINT = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
# Random variety
Variety = [
    "with a dark twist", "in a futuristic setting", "with a humorous edge",
    "in a mystical tone", "with a tragic backstory", "in an unexpected style",
    "with a heroic flair", "in a steampunk vibe", "with a chaotic spin"
]

# Craft a prompt with randomization
def craft_prompt(content_type, user_input):
    variety = random.choice(Variety)
    return f"Generate video game {content_type} content: '{user_input}' {variety}. Respond only with the content."

# Call the Gemini 1.5 Flash API (placeholder - adjust ENDPOINT and API_KEY as needed)
def call_gemini(prompt):
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": 150, # gives you a good idea to run with
            "temperature": 0.8 # ensures randomness and is readable
        }
    }
    try:
        response = requests.post(f"{ENDPOINT}?key={API_KEY}", json=data, headers=headers)
        if response.status_code == 200:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"API Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {e}"

# Main generation function
def generate_content():
    content_types = ["character", "environment", "storyline", "genre", "villain", "artifact", "faction"]
    print("\n=== Video Game Content Generator ===")
    print("What do you need help making?")
    for i, ct in enumerate(content_types, 1):
        print(f"{i}. {ct}")
    print(f"{len(content_types) + 1}. Do it for me")  # New option

    try:
        choice = int(input("Enter the number of your choice: ")) - 1
        if choice not in range(len(content_types) + 1):  # Adjusted range to include "all"
            print("Choice out of range! Pick a number from the list.")
            return
    except ValueError:
        print("Invalid input! Enter a number 1-8.")
        return

    user_input = input("What is your idea? ")

    # Check if "all" was selected
    if choice == len(content_types):  # "All" is the last option
        print("\nGenerating content for all types:\n")
        for content_type in content_types:
            prompt = craft_prompt(content_type, user_input)
            generated_text = call_gemini(prompt)
            print(f"Generated {content_type}:\n{generated_text}\n")
    else:
        content_type = content_types[choice]
        prompt = craft_prompt(content_type, user_input)
        generated_text = call_gemini(prompt)
        print(f"\nGenerated {content_type}:\n{generated_text}\n")

# Run it
if __name__ == "__main__":
    print("Neural Nexus Game Content Creator Prototype (Powered by Gemini 1.5 Flash)!")
    while True:
        generate_content()
        if input("Generate another? (y/n): ").lower() != "y":
            print("Thanks for using the prototype!")
            break