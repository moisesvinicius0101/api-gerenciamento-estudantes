

from fastapi import FastAPI

from routers.student import router as student_router
from routers.courses import router as courses_router
from database import Base, engine
import models  # noqa: F401

# CONFIGURAÇÃO DA API

app = FastAPI(
    title="Api Para Gerenciamento de Estudantes e Cursos",
    description="Api simples para gerenciar estudantes e cursos"
)
app.include_router(student_router)
app.include_router(courses_router)

Base.metadata.create_all(bind=engine)

