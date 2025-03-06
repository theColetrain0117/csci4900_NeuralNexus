import random
import requests
import pyodbc
import os
import openai
from db_config import db_config

# Load API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ENDPOINT = "https://api.openai.com/v1/completions"


# Database connection
def get_db_connection():
    conn_str = (
        f"DRIVER={{SQL Server}};"
        f"SERVER={db_config['server']};"
        f"DATABASE={db_config['database']};"
        f"UID={db_config['username']};"
        f"PWD={db_config['password']}"
    )
    return pyodbc.connect(conn_str)


# Generate prompt with randomization
Variety = [
    "with a dark twist", "in a futuristic setting", "with a humorous edge",
    "in a mystical tone", "with a tragic backstory", "in an unexpected style",
    "with a heroic flair", "in a steampunk vibe", "with a chaotic spin"
]

def craft_prompt(content_type, user_input):
    variety = random.choice(Variety)
    return f"Generate video game {content_type} content: '{user_input}' {variety}. Respond only with the content."


# Call OpenAI API
def call_open_ai(prompt):
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": 150,
            "temperature": 0.8
        }
    }
    try:
        response = requests.post(f"{OPENAI_ENDPOINT}?key={OPENAI_API_KEY}", json=data, headers=headers)
        if response.status_code == 200:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"API Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {e}"


# Generate OpenAI response
def generate_ai_response(prompt):
    response = openai.Completion.create(
        engine="gpt-4o-mini",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()


# Main generation class
class AIGenerator:
    def __init__(self):
        self.genres = ["fantasy", "sci-fi", "horror"]
        self.story_templates = {
            "fantasy": "A {hero} must {quest} to save {place} from {villain}.",
            "sci-fi": "In {year}, a {hero} uncovers {mystery} on {place}.",
            "horror": "A {hero} is trapped in {place}, hunted by {villain}."
        }
        self.characters = ["warrior", "scientist", "detective"]
        self.traits = ["brave", "curious", "haunted"]
        self.places = {
            "fantasy": "an enchanted forest",
            "sci-fi": "a distant planet",
            "horror": "an abandoned asylum"
        }
        self.villains = ["a dark sorcerer", "a rogue AI", "a spectral entity"]

    def get_content_by_genre(self, genre):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT TOP 1 content_id, storyline FROM Content WHERE genre = ? ORDER BY NEWID()"
        cursor.execute(query, (genre,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return {"content_id": result[0], "storyline": result[1]} if result else None

    def generate_content(self, user_id, ai_model_id, genre):
        if genre not in self.genres:
            genre = random.choice(self.genres)

        # Generate storyline
        storyline = self.story_templates[genre].format(
            hero=random.choice(self.characters),
            quest="retrieve a lost artifact" if genre == "fantasy" else "stop a catastrophe",
            place=self.places[genre],
            villain=random.choice(self.villains),
            year="2247" if genre == "sci-fi" else "",
            mystery="a rogue AI" if genre == "sci-fi" else ""
        )

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert into database
        content_query = """
            INSERT INTO Content (user_id, ai_model_id, genre, storyline)
            VALUES (?, ?, ?, ?);
            SELECT SCOPE_IDENTITY() AS last_id;
        """
        cursor.execute(content_query, (user_id, ai_model_id, genre, storyline))
        content_id = int(cursor.fetchone()[0])

        conn.commit()
        cursor.close()
        conn.close()

        return {"content_id": content_id, "storyline": storyline}


# Main script
if __name__ == "__main__":
    ai_generator = AIGenerator()
    print("Neural Nexus Game Content Creator (Unified Version)!")

    user_input = input("Enter your idea for the content: ")
    genre = input("Enter a genre (fantasy, sci-fi, horror): ")
    user_id = 1
    ai_model_id = 1

    content = ai_generator.generate_content(user_id, ai_model_id, genre)
    print(f"Generated Content:\n{content}")
