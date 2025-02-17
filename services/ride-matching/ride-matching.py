import uvicorn
from fastapi import FastAPI
from src.web import ride_matching
from fastapi.middleware.cors import CORSMiddleware


origins = [
    "http://localhost:8004"
    #"*", //allow all
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["+"],
    allow_headers=["+"],
)

app.include_router(ride_matching.router, tags =["Ride_matching"])

if __name__ == "__main__":
    uvicorn.run("ride_matching:app", reload=True, host="0.0.0.0", port=8004)