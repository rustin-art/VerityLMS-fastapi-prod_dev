from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

database_url = 'sqlite:///./notes.db'

print("!<----Initializing Request to Database")
engine = create_engine(database_url, connect_args={'check_same_thread': False})

print("!<----Initializing Session with Database---->!")
SessionLocal = sessionmaker(autoflush=False, autocommit=False,bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
