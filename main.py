# main.py
from fastapi import FastAPI, HTTPException
from ai_generator import AIGenerator

app = FastAPI()

db_config = {
    "server": "COLEHOME",
    "database": "GenAIProject",
    "username": "name",
    "password": "your_password"
}

ai_generator = AIGenerator(db_config)

@app.get("/content/{genre}")
async def get_content(genre: str):
    content = ai_generator.get_content_by_genre(genre)
    if content:
        return content
    else:
        raise HTTPException(status_code=404, detail="Content not found")

@app.post("/generate/")
async def generate_content(user_id: int, ai_model_id: int, genre: str):
    result = ai_generator.generate_content(user_id, ai_model_id, genre)
    return result

@app.post("/ai-response/")
async def ai_response(prompt: str):
    response = generate_ai_response(prompt)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
