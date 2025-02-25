from fastapi import FastAPI, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
import httpx
import uvicorn
from src.model.schemas import LoginRequest
from fastapi.middleware.cors import CORSMiddleware


# Define services
service = {
    "user": "http://localhost:8001",
    "rider": "http://localhost:8002"
}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  #Allow all HTTP methods, including OPTIONS
    allow_headers=["*"],  #Allow all headers
)


async def forward_request(service_url: str, method: str, path: str, body=None, headers=None):
    """
    Handles forwarding API requests to the appropriate microservice.
    """
    async with httpx.AsyncClient() as client:
        response = await client.request(method, f"{service_url}{path}", json=body, headers=headers)
        return response


# ✅ **User Login (Gateway forwards request to User Service)**
@app.post("/gateway/login/user")
async def login_user(login_data: LoginRequest):
    """
    API Gateway login endpoint for Users.
    """
    service_url = service["user"]
    response = await forward_request(service_url, "POST", "/login", login_data.dict(), None)

    if response.status_code == 404:
        return JSONResponse(status_code=404, content={"detail": "User account not found. Please register at /users/register"})

    return JSONResponse(content=response.json(), status_code=response.status_code)



@app.post("/gateway/login/rider")
async def login_rider(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    API Gateway login endpoint for Riders.
    """
    service_url = service["rider"]
    print(f"🔍 Forwarding rider login request to {service_url}/riders/login")

    # ✅ Convert form-data to dictionary
    login_data = {"username": form_data.username, "password": form_data.password}

    response = await forward_request(service_url, "POST", "/riders/login", login_data, None)

    print(f"🔍 Response from Rider Service: {response.status_code}, {response.json()}")

    if response.status_code == 404:
        return JSONResponse(
            status_code=404, 
            content={"detail": "Rider account not found. Please register at /riders/register"}
        )

    return JSONResponse(content=response.json(), status_code=response.status_code)


if __name__ == "__main__":
    uvicorn.run("api:app", reload=True, host="0.0.0.0", port=8000)
