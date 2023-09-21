from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal: Session = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

SqlAlchemyBase = declarative_base()


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


from .models import Product, Role, User
