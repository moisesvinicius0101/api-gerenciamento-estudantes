
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from dependencies import get_current_user
from routers import auth, courses, student
import models  # noqa: F401


tags_metadata = [
    {
        "name": "auth",
        "description": "Cadastro e login de usuários. Gera o **token JWT** usado nas demais rotas.",
    },
    {
        "name": "students",
        "description": "Gerenciamento de **estudantes**. Cada estudante pode estar vinculado a um curso.",
    },
    {
        "name": "courses",
        "description": "Gerenciamento de **cursos**. Um curso pode ter vários estudantes.",
    },
]

DESCRIPTION = """
API REST para gerenciar **estudantes** e **cursos**, com autenticação via **JWT**.

## Como usar

1. Crie um usuário em `POST /auth/register`
2. Clique em **Authorize** e informe seu e-mail (em `username`) e senha
3. Use as rotas protegidas de **students** e **courses**

## Recursos

* CRUD completo de estudantes e cursos
* Relacionamento 1:N entre cursos e estudantes
* Autenticação com token Bearer
* Senhas protegidas com hash Argon2
"""

app = FastAPI(
    title="API de Gerenciamento de Estudantes e Cursos",
    summary="CRUD de estudantes e cursos com autenticação JWT.",
    description=DESCRIPTION,
    version="1.0.0",
    openapi_tags=tags_metadata,
    contact={
        "name": "Moisés Vinícius",
        "url": "https://github.com/moisesvinicius0101",
    },
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
    swagger_ui_parameters={
        "persistAuthorization": True,    # mantém o login ao recarregar a página
        "displayRequestDuration": True,  # mostra o tempo de cada requisição
        "filter": True,                  # campo de busca de rotas
        "docExpansion": "none",          # começa com as rotas recolhidas
        "defaultModelsExpandDepth": -1,  # esconde a seção "Schemas" no final
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(student.router, dependencies=[Depends(get_current_user)])
app.include_router(courses.router, dependencies=[Depends(get_current_user)])

Base.metadata.create_all(bind=engine)