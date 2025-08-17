import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import openai

AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if AI_PROVIDER == "openai" and OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SummaryRequest(BaseModel):
    transcript: str
    prompt: str

@app.post("/generate_summary")
async def generate_summary(req: SummaryRequest):
    if AI_PROVIDER == "openai":
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI that summarizes meeting notes."},
                {"role": "user", "content": f"Transcript:\n{req.transcript}\n\nInstruction: {req.prompt}"}
            ]
        )
        summary = response["choices"][0]["message"]["content"]
    else:
        summary = f"(Demo) Summary generated for: {req.prompt}"
    return {"summary": summary}

@app.get("/")
async def serve_frontend():
    return FileResponse("public/index.html")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
