

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CourseInStudent(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    carga_horaria: int


class StudentCreate(BaseModel):
    nome: str = Field(..., min_length=3, max_length=50)
    idade: int = Field(..., ge=0)
    email: EmailStr
    course_id: int | None = None   


class UpdateStudent(BaseModel):
    nome: str | None = Field(default=None, min_length=3, max_length=50)
    idade: int | None = Field(default=None, ge=0)
    email: EmailStr | None = None
    course_id: int | None = None   


class ResponseStudent(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    idade: int
    email: EmailStr
    course_id: int | None = None   
    course: CourseInStudent | None = None

