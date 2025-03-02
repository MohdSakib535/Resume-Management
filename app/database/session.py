from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Without get_db(), you would need to manually open and close the session in every route:

def get_db():
    db = SessionLocal() # Create a new database session
    try:
        yield db   # Provide the session to the route
    finally:
        db.close()   # Close the session after request is complete
