

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.users import User
from utill.security import hash_password, verify_password

# Hash falso, usado para gastar o mesmo tempo quando o e-mail não existe
_DUMMY_HASH = hash_password("senha-falsa-para-igualar-tempo")


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email.lower()))


def create_user(db: Session, email: str, password: str) -> User | None:
    if get_user_by_email(db, email):
        return None

    new_user = User(email=email.lower(), hashed_password=hash_password(password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if not user:
        verify_password(password, _DUMMY_HASH)
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user