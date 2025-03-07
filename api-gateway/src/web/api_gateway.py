from fastapi import APIRouter, HTTPException, Depends, Security, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from src.model.rider import AvailabilityUpdate, RiderResponse
import httpx
import os
from src.service.security import rider_oauth2_scheme
from typing import List


# Service URLs from environment variables (with defaults)
service = {
    "user": os.getenv("USER_SERVICE_URL", "http://localhost:8001"),
    "rider": os.getenv("RIDER_SERVICE_URL", "http://localhost:8002"),
}

rider_router = APIRouter()
user_router = APIRouter()


async def forward_request(service_url: str, method: str, path: str, body=None, headers=None):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.request(
            method,
            f"{service_url}{path}",
            json=body,
            headers=headers
        )
        return response


@rider_router.post("/gateway/login/rider")
async def login_rider(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    API Gateway login endpoint for Riders.
    Forwards the login request to the Rider Service and creates a gateway JWT token.
    """
    service_url = service["rider"]
    print(f"🔍 Forwarding rider login request to {service_url}/riders/login")

    login_data = {"username": form_data.username, "password": form_data.password}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{service_url}/riders/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

    if response.status_code != 200:
        if response.status_code == 404:
            return JSONResponse(
                status_code=404,
                content={"detail": "Rider account not found. Please register first."}
            )
        return JSONResponse(content=response.json(), status_code=response.status_code)


@rider_router.get("/gateway/riders", response_model=List[RiderResponse])
async def gateway_get_riders():
    """
    Forwards a GET request to retrieve all riders from the Rider Service.
    """
    response = await forward_request(service["rider"], "GET", "/riders")
    return JSONResponse(content=response.json(), status_code=response.status_code)

@rider_router.put("/gateway/riders/{rider_id}/availability")
async def gateway_update_availability(
    rider_id: int,
    availability: AvailabilityUpdate,
    current_rider: dict = Depends(get_current_rider)
):
    """
    API Gateway endpoint to update rider availability.
    """
    service_url = service["rider"]
    is_available = availability.is_available
    
    # Forward the request with the rider's token
    response = await forward_request(
        service_url,
        "PUT",
        f"/riders/{rider_id}/availability?is_available={is_available}",
        headers={"Authorization": f"Bearer {current_rider['username']}"}
    )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return JSONResponse(content=response.json(), status_code=response.status_code)