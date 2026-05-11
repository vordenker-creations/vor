from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

# Get Database URL from environment variable, default to local if not set
# Use "db" instead of "localhost" when running inside Docker
DEFAULT_DB_URL = "postgresql://vor:coolpassword1234@localhost:5432/aicareer_bridge"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB_URL)

# The Engine establishes the physical connection to the database
engine = create_engine(DATABASE_URL, echo=False)

# The Session is what FastAPI will use to execute queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Modern SQLAlchemy 2.0 Base class
class Base(DeclarativeBase):
    pass
 
# Dependency function for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
