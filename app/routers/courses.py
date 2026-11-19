


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated 
from crud import courses
from schemas.courses_schemas import CourseCreate, CourseUpdate

from database import get_db
# schemas 


router = APIRouter(
    prefix="/courses",
    tags=["courses"]
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/", status_code=status.HTTP_200_OK)
def get_all_courses(db: db_dependency):
    return courses.get_all_courses(db)

@router.get("/{id_course}", status_code=status.HTTP_200_OK)
def get_course_by_id(id_course: int, db: db_dependency):
    course = courses.get_course_by_id(db, id_course)

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Curso não encontrado"
            )
    
    return course

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_course(db: db_dependency, data_course: CourseCreate):

    course = create_course(db, data_course)

    if not course:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Curso já cadastrado"
            )
    
    return course

@router.put("/{id_course}", status_code=status.HTTP_200_OK)
def update_course(id_course: int, db: db_dependency, data_course: CourseUpdate):
    course = update_course(db, id_course, data_course)

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Curso não encontrado"
            )

    return course

@router.delete("/{id_course}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(id_course: int, db: db_dependency):
    course = delete_course(db, id_course)

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso não encontrado"
        )



