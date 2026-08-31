from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import settings

# SQLAlchemy setup for Supabase Postgres
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Dependency helper providing a database session lifecycle per request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()