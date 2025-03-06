from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from src.web.api_gateway import router as api_router


# Define services
service = {
    "user": "http://localhost:8001",
    "rider": "http://localhost:8002",
    "booking": "http://localhost:8003",
    "ride_matching": "http://localhost:8004",
}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  #Allow all HTTP methods, including OPTIONS
    allow_headers=["*"],  #Allow all headers
)

app.include_router(api_router, tags=["Gateway"])


if __name__ == "__main__":
    uvicorn.run("api:app", reload=True, host="0.0.0.0", port=8000)