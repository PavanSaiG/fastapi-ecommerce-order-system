from sqlalchemy.orm import sessionmaker
from app.database.db import engine

# Create a customized SessionLocal class using sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
