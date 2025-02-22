from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pathlib import Path
from src.web import rider
from src.data import models, init

# Load environment variables
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Create database tables
models.Base.metadata.create_all(bind=init.engine)

origins = ("http://localhost:8003",)

app = FastAPI(
    title="Rider Service",
    description="Rider management service",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(rider.router, tags=["Rider"])

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Rider Service...")
    print("📚 Swagger UI will be available at: http://localhost:8002/docs")
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True, reload_dirs=["src"])
