import pyodbc
import random

class AIGenerator:
    def __init__(self, db_config):
        self.db_config = db_config
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

    def _get_db_connection(self):
        """Connects to MSSQL database."""
        conn_str = (
            f"DRIVER={{SQL Server}};"
            f"SERVER={self.db_config['server']};"
            f"DATABASE={self.db_config['database']};"
            f"UID={self.db_config['username']};"
            f"PWD={self.db_config['password']}"
        )
        return pyodbc.connect(conn_str)

    def get_content_by_genre(self, genre):
        """Pull existing content from the database by genre."""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        query = "SELECT TOP 1 content_id, storyline FROM Content WHERE genre = ? ORDER BY NEWID()"
        cursor.execute(query, (genre,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return {"content_id": result[0], "storyline": result[1]}
        return None





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

    # Generate character
    char_name = random.choice(["Elara", "Jaxon", "Mira"])
    char_role = random.choice(self.characters)
    char_trait = random.choice(self.traits)

    # Generate environment
    env_desc = f"A {random.choice(['vast', 'eerie', 'futuristic'])} {self.places[genre]} with {random.choice(['glowing crystals', 'rusted machinery', 'flickering lights'])}."

    # Save to database
    conn = self._get_db_connection()
    cursor = conn.cursor()

    # Insert into Content
    content_query = """
        INSERT INTO Content (user_id, ai_model_id, genre, storyline)
        VALUES (?, ?, ?, ?);
        SELECT SCOPE_IDENTITY() AS last_id;
    """
    cursor.execute(content_query, (user_id, ai_model_id, genre, storyline))
    content_id = int(cursor.fetchone()[0])

    # Insert into Character
    char_query = """
        INSERT INTO [Character] (content_id, user_id, name, role, trait)
        VALUES (?, ?, ?, ?, ?);
        SELECT SCOPE_IDENTITY() AS last_id;
    """
    cursor.execute(char_query, (content_id, user_id, char_name, char_role, char_trait))
    char_id = int(cursor.fetchone()[0])

    # Insert into EnvironmentModel
    env_query = """
        INSERT INTO EnvironmentModel (content_id, user_id, description, model_file_path, file_format)
        VALUES (?, ?, ?, ?, ?);
        SELECT SCOPE_IDENTITY() AS last_id;
    """
    cursor.execute(env_query, (content_id, user_id, env_desc, None, None))
    env_id = int(cursor.fetchone()[0])

    conn.commit()
    cursor.close()
    conn.close()

    return {
        "content_id": content_id,
        "storyline": storyline,
        "character": {"id": char_id, "name": char_name, "role": char_role, "trait": char_trait},
        "environment": {"id": env_id, "description": env_desc}
    }
def main():
    # Database config
    db_config = {
        "server": "COLEHOME",
        "database": "GenAIProject",
        "username": "name",
        "password": "your_password"
    }

    ai = AIGenerator(db_config)
    user_id = 1  # Hardcoded for now; assume user_id 1 exists
    ai_model_id = 1  # Hardcoded; assume ai_model_id 1 exists

    while True:
        print("\nAI Game Dev Tool")
        print("1. View existing content by genre")
        print("2. Generate new content")
        print("3. Quit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            genre = input("Enter genre (fantasy, sci-fi, horror): ").lower()
            content = ai.get_content_by_genre(genre)
            if content:
                print(f"Content ID: {content['content_id']}")
                print(f"Storyline: {content['storyline']}")
            else:
                print(f"No content found for genre '{genre}'.")

        elif choice == "2":
            genre = input("Enter genre (fantasy, sci-fi, horror): ").lower()
            result = ai.generate_content(user_id, ai_model_id, genre)
            print(f"\nGenerated Content (ID: {result['content_id']}):")
            print(f"Storyline: {result['storyline']}")
            print(f"Character (ID: {result['character']['id']}): Name: {result['character']['name']}, Role: {result['character']['role']}, Trait: {result['character']['trait']}")
            print(f"Environment (ID: {result['environment']['id']}): {result['environment']['description']}")

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
