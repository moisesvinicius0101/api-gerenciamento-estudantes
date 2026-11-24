

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String, nullable=False)
    idade: Mapped[int] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )

    course_id: Mapped[int | None] = mapped_column(
        ForeignKey("courses.id"), nullable=True
    )

    course = relationship("Course", back_populates="students")

    
