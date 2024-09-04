from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import sys

SQLALCHEMY_DATABASE_URL = "postgresql://adminSenvoDB:senvo2024@db:5432/SenvoAPI"

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    print("Connected to the database!")
except Exception as e:
    print(f"Error connecting to database: {e}")
    sys.exit(1)

Base = declarative_base()


def db():
    database = SessionLocal()
    try:
        print("Starting up...")
        yield database
    finally:
        print("Shutting down...")
        database.close()
