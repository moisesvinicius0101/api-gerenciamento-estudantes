
from sqlalchemy.orm import Session
from sqlalchemy import select

from models.students import Student
from models.courses import Course

from schemas.student_schemas import StudentCreate, UpdateStudent


def get_all_students(db: Session):
    query = select(Student)
    return db.scalars(query).all()


def filter_students(db: Session, nome: str | None, curso: str | None):
    query = select(Student)

    if nome:
        query = query.where(Student.nome.ilike(f"%{nome}%"))

    if curso:
        query = query.join(Course).where(Course.title.ilike(f"%{curso}%"))

    return db.scalars(query).unique().all()

def get_student_by_id(db: Session, id_student):
    return db.get(Student, id_student)


def create_student(db: Session, data_student: StudentCreate):
    query = select(Student).where(Student.email == str(data_student.email))
    if db.scalar(query):
        return None

    # valida o curso, se foi informado
    if data_student.course_id is not None:
        course = db.get(Course, data_student.course_id)
        if not course:
            return "course_not_found"

    new_student = Student(
        nome=data_student.nome,
        idade=data_student.idade,
        email=str(data_student.email),
        course_id=data_student.course_id,  
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

def update_student(db: Session, id_student, student: UpdateStudent):
    student_db = db.get(Student, id_student)
    if not student_db:
        return None

    values = student.model_dump(exclude_unset=True)

    for key, value in values.items():
        value = str(value) if key == "email" and value is not None else value
        if key == "email":
            existing = db.scalar(
                select(Student).where(
                    Student.email == value,
                    Student.id != id_student,
                )
            )
            if existing:
                raise ValueError("Email já cadastrado")
        setattr(student_db, key, value)


    db.commit()
    db.refresh(student_db)
    return student_db

def delete_student(db: Session, id_student):
    student_db = db.get(Student, id_student)
    if not student_db:
        return None

    db.delete(student_db)
    db.commit()
    return student_db

