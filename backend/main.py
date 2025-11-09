"""
FastAPI application exposing endpoints per spec.

Endpoints:
 - POST /generate_quiz  { url }
 - GET /history
 - GET /quiz/{quiz_id}

Uses async SQLAlchemy sessions and stores quizzes in DB.
"""
import os
import json
from typing import Any, Dict
import asyncio

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl

from dotenv import load_dotenv

load_dotenv()

from database import engine, Base, get_db, AsyncSessionLocal
from models import Quiz
from scraper import scrape_wikipedia
from llm_quiz_generator import generate_quiz

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

app = FastAPI(title="AI Wiki Quiz Generator")

FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateRequest(BaseModel):
    url: str  # Changed from HttpUrl to str for more flexibility
    extra_questions: bool = False  # Add 5 extra questions if True


@app.on_event("startup")
async def startup_event():
    # Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"message": "AI Wiki Quiz Generator API"}


@app.post("/generate_quiz")
async def generate_quiz_endpoint(payload: GenerateRequest):
    url = payload.url

    # Check if we already have this quiz cached in database for speed
    # Include extra_questions in cache logic to avoid returning wrong question count
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Quiz).where(Quiz.url == url).limit(1))
        existing = result.scalar_one_or_none()
        if existing and existing.full_quiz_data:
            try:
                cached_quiz = json.loads(existing.full_quiz_data)
                # Only use cache if question count matches what user requested AND has study_summary
                expected_count = 15 if payload.extra_questions else 10
                if (len(cached_quiz.get('questions', [])) == expected_count and 
                    'study_summary' in cached_quiz):
                    return {"quiz": cached_quiz, "id": existing.id, "cached": True}
            except:
                pass  # If cached data is invalid, continue with fresh generation

    # Scrape with better error handling
    try:
        title, text = await asyncio.get_event_loop().run_in_executor(None, scrape_wikipedia, url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Generate quiz via LLM wrapper (faster processing)
    try:
        quiz_obj = await asyncio.get_event_loop().run_in_executor(
            None, generate_quiz, title, text, payload.extra_questions
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate quiz: {str(e)}")

    # Persist
    async with AsyncSessionLocal() as session:
        new = Quiz(
            url=url, 
            title=quiz_obj.get("title", title), 
            scraped_content=text, 
            full_quiz_data=json.dumps(quiz_obj)
        )
        session.add(new)
        await session.commit()
        await session.refresh(new)

        return {"quiz": quiz_obj, "id": new.id, "cached": False}


@app.get("/history")
async def history(skip: int = 0, limit: int = 100):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Quiz).offset(skip).limit(limit).order_by(Quiz.date_generated.desc()))
        rows = result.scalars().all()
        return {"quizzes": [r.to_dict() for r in rows]}


@app.get("/quiz/{quiz_id}")
async def get_quiz(quiz_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Quiz).where(Quiz.id == quiz_id))
        row = result.scalar_one_or_none()
        if not row:
            raise HTTPException(status_code=404, detail="Quiz not found")
        # parse JSON field
        try:
            quiz_data = json.loads(row.full_quiz_data) if row.full_quiz_data else {}
        except Exception:
            quiz_data = {"title": row.title}
        return {
            "quiz": quiz_data, 
            "meta": {
                "id": row.id, 
                "url": row.url, 
                "title": row.title, 
                "date_generated": row.date_generated.isoformat() if row.date_generated else None
            }
        }