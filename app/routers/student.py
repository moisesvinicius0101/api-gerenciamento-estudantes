

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.student_schemas import (
    StudentCreate,
    UpdateStudent,
    ResponseStudent,
)
from typing import Annotated

from crud import student as crud

from dependencies import require_admin


router = APIRouter(
    prefix="/students",
    tags=["students"]
)

db_dependency = Annotated[Session, Depends(get_db)]


# LISTAR TODOS OS ESTUDANTES


@router.get("/", response_model=list[ResponseStudent], dependencies=[Depends(require_admin)])
def get_all(db: db_dependency):
    students = crud.get_all_students(db)
    if students:
        return students
    raise HTTPException(
        status_code=404, 
        detail="Nenhum estudante encontrado"
        )



# ==============================
# FILTRAR ESTUDANTES
# ==============================

@router.get("/search", response_model=list[ResponseStudent], dependencies=[Depends(require_admin)])
def search_students(
    db: db_dependency,
    nome: str | None = None,
    curso: str | None = None
):
    return crud.filter_students(db, nome, curso)

# ==============================
# BUSCAR ESTUDANTE POR ID
# ==============================

@router.get(
    "/{id_student}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseStudent,
    dependencies=[Depends(require_admin)]
)
def get_by_id(db: db_dependency, id_student: int):

    student = crud.get_student_by_id(db, id_student)

    if student:
        return student 
    raise HTTPException(
        status_code=404,
        detail="Nenhum estudante encontrado"
    )


# ==============================
# CRIAR ESTUDANTE
# ==============================

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseStudent,
    dependencies=[Depends(require_admin)]
)
def create_student(db: db_dependency, data_student: StudentCreate):
    try:
        student = crud.create_student(db, data_student)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

    # Mostrar mensagem de erro caso o email já exista
    if student is None:
        raise HTTPException(
            status_code=400,
            detail="Email já cadastrado"
        )

    return student
    


# ==============================
# ATUALIZAR ESTUDANTE
# ==============================

@router.put(
    "/{id_student}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseStudent,
    dependencies=[Depends(require_admin)]
)
def update_student(db: db_dependency, id_student: int, student: UpdateStudent):
    try:
        updated_student = crud.update_student(db, id_student, student)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

    if updated_student:
        return updated_student

    raise HTTPException(
        status_code=404,
        detail="Estudante não encontrado"
    )

# ==============================
# DELETAR ESTUDANTE
# ==============================

@router.delete(
    "/{id_student}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)]
)
def delete_student(db: db_dependency, id_student: int):

    student = crud.delete_student(db, id_student)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Estudante não encontrado"
        )