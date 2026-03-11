from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import random
from typing import List
import models
from database import SessionLocal, engine

# Создаем таблицы
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
     allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://histore-pet-project.vercel.app",
        "https://*.vercel.app",
        "https://*.ngrok.io",
        "http://192.168.0.5:8000"  
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Зависимость для БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Историческая викторина API 🚀"}

@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = request.headers.get("origin", "*")
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

@app.get("/api/questions/random")
def get_random_question(db: Session = Depends(get_db)):
    questions = db.query(models.Quiz).all()
    if not questions:
        raise HTTPException(status_code=404, detail="Нет вопросов")
    question = random.choice(questions)
    return question

@app.post("/api/users/auth")
def auth_user(telegram_data: dict, db: Session = Depends(get_db)):
    telegram_id = str(telegram_data.get("id"))
    user = db.query(models.User).filter(models.User.telegram_id == telegram_id).first()
    
    if not user:
        user = models.User(
            telegram_id=telegram_id,
            first_name=telegram_data.get("first_name", "Игрок"),
            username=telegram_data.get("username")
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    return user

@app.get("/api/leaderboard")
def get_leaderboard(limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.total_score.desc()).limit(limit).all()
    return users

@app.post("/api/quiz/answer")
def save_answer(answer_data: dict, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == answer_data["user_id"]).first()
    if user and answer_data["correct"]:
        user.total_score += 10
        user.games_played += 1
        db.commit()
    return {"status": "ok"}

@app.get("/api/user/{user_id}/achievements")
def get_user_achievements(user_id: int, db: Session = Depends(get_db)):
    # Пока возвращаем тестовые данные
    return [
        {"id": 1, "name": "Новичок", "description": "Сыграть первую игру", "icon": "🎮"},
        {"id": 2, "name": "Эрудит", "description": "Набрать 100 очков", "icon": "🧠"}
    ]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)