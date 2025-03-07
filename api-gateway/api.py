from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.web.api_gateway import rider_router


app = FastAPI(
    title="API Gateway",
    description="Central entry point for Users & Riders",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rider_router, tags=["Rider Gateway"])
#app.include_router(user_router, tags=["User Gateway"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)