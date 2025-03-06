from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
import httpx
from src.model.schemas import LoginRequest
import os
router = APIRouter()

service = {
    "user": os.getenv("USER_SERVICE_URL", "http://localhost:8001"),
    "rider": os.getenv("RIDER_SERVICE_URL", "http://localhost:8002"),
    "booking": os.getenv("BOOKING_SERVICE_URL", "http://localhost:8003"),
    "ride_matching": os.getenv("RIDE_MATCHING_SERVICE_URL", "http://localhost:8004"),
}


async def forward_request(service_url: str, method: str, path: str, body=None, headers=None):
    """
    Handles forwarding API requests to the appropriate microservice.
    """
    async with httpx.AsyncClient() as client:
        response = await client.request(method, f"{service_url}{path}", json=body, headers=headers)
        return response


# ✅ **User Login (Gateway forwards request to User Service)**
@router.post("/gateway/login/user")
async def login_user(login_data: LoginRequest):
    """
    API Gateway login endpoint for Users.
    """
    service_url = service["user"]
    response = await forward_request(service_url, "POST", "/login", login_data.dict(), None)

    if response.status_code == 404:
        return JSONResponse(status_code=404, content={"detail": "User account not found. Please register at /users/register"})

    return JSONResponse(content=response.json(), status_code=response.status_code)



@router.post("/gateway/login/rider")
async def login_rider(form_data: OAuth2PasswordRequestForm = Depends()):
    service_url = service["rider"]
    login_data = {
        "username": form_data.username,
        "password": form_data.password
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{service_url}/riders/login",
            data=login_data,  # Send as form data
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

    return JSONResponse(content=response.json(), status_code=response.status_code)
