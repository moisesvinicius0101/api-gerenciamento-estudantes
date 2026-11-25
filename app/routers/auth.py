

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from crud import users as crud_users
from database import get_db
from dependencies import CurrentUser
from schemas.user_schemas import Token, UserCreate, UserResponse, UserRoleUpdate
from utill.security import create_access_token

from models.users import User, UserRole
from dependencies import AdminUser

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register(data: UserCreate, db: Annotated[Session, Depends(get_db)]):
    user = crud_users.create_user(db, str(data.email), data.password)
    if not user:
        raise HTTPException(status_code=409, detail="E-mail já cadastrado")
    return user


@router.post("/login", response_model=Token)
def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    user = crud_users.authenticate_user(db, form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=create_access_token(user.id))


@router.get("/me", response_model=UserResponse)
def me(current_user: CurrentUser):
    return current_user

@router.patch("/users/{user_id}/role", response_model=UserResponse)
def change_role(
    user_id: int,
    data: UserRoleUpdate,
    admin: AdminUser,
    db: Annotated[Session, Depends(get_db)],
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if user.id == admin.id and data.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=400, detail="Você não pode remover seu próprio acesso de admin"
        )
    return crud_users.update_user_role(db, user, data.role)
