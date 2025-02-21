# Added code to load environment variables from Coursework/.env
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.web import user
from src.data import models, init

# Create database tables
models.Base.metadata.create_all(bind=init.engine)

origins = ("http://localhost:8003",)

app = FastAPI(
    title="User Service",
    description="User management service",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user.router, tags=["User"])
app.include_router(user.auth_router, tags=["Auth"])

if __name__ == "__main__":
    print("🚀 Starting User Service...")
    print("📚 Swagger UI will be available at: http://localhost:8001/docs")
    print("🔄 ReDoc will be available at: http://localhost:8001/redoc")
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True, reload_dirs=["src"]) 