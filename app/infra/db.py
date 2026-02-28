from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://user:password@localhost:5432/market"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)