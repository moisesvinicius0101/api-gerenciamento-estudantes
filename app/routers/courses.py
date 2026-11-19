


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated 

from database import get_db
# schemas 


router = APIRouter(
    prefix="/courses",
    tags=["courses"]
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/", status_code=status.HTTP_200_OK)
def get_all_courses(db: db_dependency):
    pass 

@router.get("/{id_course}", status_code=status.HTTP_200_OK)
def get_course_by_id(id_course: int, db: db_dependency):
    pass

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_course(db: db_dependency):
    pass

@router.put("/{id_course}", status_code=status.HTTP_200_OK)
def update_course(id_course: int, db: db_dependency):
    pass

@router.delete("/{id_course}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(id_course: int, db: db_dependency):
    pass



