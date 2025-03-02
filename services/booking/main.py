from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pathlib import Path
import os
from src.web import booking
from src.data import models, init

# Load environment variables
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    print("Warning: .env file not found, using default environment variables.")

#Use Alembic for better control)
models.Base.metadata.create_all(bind=init.engine)

# CORS Configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:8003").split(",")

app = FastAPI(
    title="Booking Service",
    description="Ride booking and management service",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Register Routers
app.include_router(booking.router, tags=["booking"])

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Booking Service...")
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("BOOKING_PORT", 8004)), reload=True)
