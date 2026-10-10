
from test_database import test_engine

with test_engine.connect() as connection:
    print("Test database connection successful!")
