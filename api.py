# api.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Resume Skills API")

# Простой словарь навыков для детекции (stub).
# В проде — словарь/регулярки/векторизация.
KNOWN_SKILLS = {
    "python", "fastapi", "aiogram", "telegram", "docker",
    "redis", "postgresql", "postgre", "sql", "pandas",
    "nlp", "llm", "gpt", "rest", "asyncio", "linux",
}

class ResumeIn(BaseModel):
    text: str

class SkillsOut(BaseModel):
    skills: List[str]

@app.post("/extract_skills", response_model=SkillsOut)
def extract_skills(payload: ResumeIn):
    text = payload.text.lower()
    skills = sorted({s for s in KNOWN_SKILLS if s in text})
    return SkillsOut(skills=skills)
