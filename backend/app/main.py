from fastapi import FastAPI
from .routers import users, tasks
from .database import Base, engine

# Автосоздание таблиц в базе данных
Base.metadata.create_all(bind=engine)
app = FastAPI()

# Подключаем маршруты из модуля users с префиксом /users
app.include_router(users.router, prefix="/users", tags=["users"])

# Подключаем маршруты из модуля tasks с префиксом /tasks
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
