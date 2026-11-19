

from pydantic import BaseModel, Field


class CourseBase(BaseModel):
    title: str = Field(..., example="Introdução ao Python")
    description: str = Field(..., example="Curso introdutório ao Python.")

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int

    class Config:
        orm_mode = True