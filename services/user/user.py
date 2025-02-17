import uvicorn
from fastapi import FastAPI
from src.web import user
from fastapi.middleware.cors import CORSMiddleware


origins = [
    "http://localhost:8001"
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

app.include_router(user.router, tags =["User"])

if __name__ == "__main__":
    uvicorn.run("user:app", reload=True, host="0.0.0.0", port=8001)