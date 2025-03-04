import uvicorn
from fastapi import FastAPI
from src.web import ride_matching

app = FastAPI(
    title="Ride Matching Service",
    description="This service finds the nearest available rider and assigns them to users.",
    version="1.0.0"
)

app.include_router(ride_matching.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8003)
