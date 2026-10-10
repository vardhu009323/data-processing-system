
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

TEST_DATABASE_URL = DATABASE_URL.rsplit("/", 1)[0] + "/data_processing_test"

test_engine = create_engine(TEST_DATABASE_URL)

TestSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False
)


from database import Base
from models import Job

Base.metadata.create_all(bind=test_engine)

print("Test database tables created successfully!")
