

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


# Configuração do banco de dados
DATABASE_URL = "sqlite:///./school.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# Configuração das sessões
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


# Classe base dos models
class Base(DeclarativeBase):
    pass


# Dependência para conexão com o banco
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
