from fastapi import Depends, FastAPI
from database import Base, engine
from dependencies import get_current_user
from routers import auth, courses, student
import models 

app = FastAPI(
    title="Api Para Gerenciamento de Estudantes e Cursos",
    description="Api simples para gerenciar estudantes e cursos",
)

app.include_router(auth.router)
app.include_router(student.router, dependencies=[Depends(get_current_user)])
app.include_router(courses.router, dependencies=[Depends(get_current_user)])

Base.metadata.create_all(bind=engine)