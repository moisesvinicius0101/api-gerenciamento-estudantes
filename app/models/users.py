import enum
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class UserRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(
      Enum(
        UserRole,
        native_enum=False,
        length=20,
        values_callable=lambda e: [m.value for m in e],
    
      ),

      default=UserRole.USER,
      server_default=UserRole.USER.value,
      nullable=False,
    )

    