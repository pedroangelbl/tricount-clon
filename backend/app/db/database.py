from typing import Generator

from app.core.config import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Conexion con la base de datos(sqlite)
engine = create_engine(DATABASE_URL, echo=True) # echo para ver el sql en consola

# Configuracion de la sesion con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Devuelve la sesion creada
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
