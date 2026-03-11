from database import SessionLocal
from models import Quiz

db = SessionLocal()

questions = [
    {
        "question": "В каком году произошло крещение Руси?",
        "option_a": "862",
        "option_b": "988", 
        "option_c": "1054",
        "option_d": "1237",
        "correct_answer": "B",
        "difficulty": "easy",
        "era": "древняя_русь"
    },
    {
        "question": "Кто был первым президентом США?",
        "option_a": "Томас Джефферсон",
        "option_b": "Джордж Вашингтон",
        "option_c": "Авраам Линкольн",
        "option_d": "Бенджамин Франклин",
        "correct_answer": "B",
        "difficulty": "easy",
        "era": "новая_история"
    },
    # Добавь еще вопросов!
]

for q in questions:
    quiz = Quiz(**q)
    db.add(quiz)

db.commit()
print(f"Добавлено {len(questions)} вопросов")