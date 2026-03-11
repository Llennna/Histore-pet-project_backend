from database import engine
import models

print("Создаю таблицы...")
models.Base.metadata.create_all(bind=engine)
print("Готово!")