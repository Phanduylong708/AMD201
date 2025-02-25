from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Kết nối tới cơ sở dữ liệu PostgreSQL
user = "postgres"
password = "123"
host = "localhost"
port = "5432"
database = "rideshare"  # Sử dụng chung database với các dịch vụ khác
SQLALCHEMY_DATABASE_URL = f'postgresql://{user}:{password}@{host}:{port}/{database}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Hàm để lấy phiên làm việc với database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
