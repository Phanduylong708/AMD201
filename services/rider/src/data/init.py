from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from src.data.models import Base

# Define connection parameters similar to explorer's simplicity
user = "postgres"
password = "123"
host = "localhost"
port = "5432"
database = "rideshare"  # using 'rideshare' as the database name for User Service
SQLALCHEMY_DATABASE_URL = f'postgresql://{user}:{password}@{host}:{port}/{database}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Ensure the database tables are created
def create_tables():
    inspector = inspect(engine)
    if not inspector.has_table("riders"):
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")
    else:
        print("Tables already exist!")

# Create tables when the module is imported
create_tables()