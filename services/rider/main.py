from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pathlib import Path
from src.web.rider import router as rider_router
from src.data import models, init


# Load environment variables
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


# Create database tables
models.Base.metadata.create_all(bind=init.engine)


#Use list format for CORS origins
origins = ["http://localhost:8003"]

app = FastAPI(
    title="Rider Service",
    description="Rider management service",
    version="1.0.0"
)


# ✅ Allow All Origins for Testing (You Can Restrict It Later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ✅ Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # ✅ Allow all methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # ✅ Allow all headers
)


# ✅ Register Rider Routes
app.include_router(rider_router)


# ✅ Print all registered routes for debugging
@app.on_event("startup")
async def list_routes():
    print("\n🚀 Registered Routes in Rider Service:")
    for route in app.routes:
        print(f"➡ {route.path} ({', '.join(route.methods)})")
    print("\n")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Rider Service...")
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True, reload_dirs=["src"])
