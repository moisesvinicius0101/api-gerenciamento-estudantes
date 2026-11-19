
from sqlalchemy.orm import Session
from sqlalchemy import select

from models.courses import Course

from schemas.courses_schemas import CourseCreate, CourseUpdate 


def get_all_courses(db: Session):
    query = select(Course)
    return db.scalars(query).all()

def get_course_by_id(db: Session, id_course):
    return db.get(Course, id_course)

def create_course(db: Session, data_course: CourseCreate):
    query = select(Course).where(Course.name == str(data_course.title))
    if db.scalar(query):
        return None 

    new_course = Course(
        name=data_course.title,
        description=data_course.description
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

def update_course(db: Session, id_course, course: CourseUpdate):
    course_db = db.get(Course, id_course)
    if not course_db:
        return None

    values = course.model_dump(exclude_unset=True)

    for key, value in values.items():
        if key == "title":
            existing = db.scalar(
                select(Course).where(
                    Course.name == value,
                    Course.id != id_course,
                )
            )
            if existing:
                raise ValueError("Curso já cadastrado")
            setattr(course_db, "name", value)
        else:
            setattr(course_db, key, value)

    db.commit()
    db.refresh(course_db)
    return course_db

def delete_course(db: Session, id_course):
    course_db = db.get(Course, id_course)
    if not course_db:
        return None

    db.delete(course_db)
    db.commit()
    return True


