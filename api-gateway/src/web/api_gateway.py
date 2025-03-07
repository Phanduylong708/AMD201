from fastapi import APIRouter, HTTPException, Depends, Security, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from src.model.rider import AvailabilityUpdate
import httpx
import os
from src.service.security import rider_oauth2_scheme


# Service URLs from environment variables (with defaults)
service = {
    "user": os.getenv("USER_SERVICE_URL", "http://localhost:8001"),
    "rider": os.getenv("RIDER_SERVICE_URL", "http://localhost:8002"),
    "booking": os.getenv("BOOKING_SERVICE_URL", "http://localhost:8003"),
    "ride_matching": os.getenv("RIDE_MATCHING_SERVICE_URL", "http://localhost:8004"),
}

rider_router = APIRouter()


async def forward_request(service_url: str, method: str, path: str, body=None, headers=None):
    async with httpx.AsyncClient() as client:
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
    Forwards the login request (as form data) to the Rider Service.
    """
    service_url = service["rider"]
    print(f"🔍 Forwarding rider login request to {service_url}/riders/login")

    # Convert form data to dictionary and send as form data
    login_data = {"username": form_data.username, "password": form_data.password}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{service_url}/riders/login",
            data=login_data,  # using form data
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

    print(f"🔍 Response from Rider Service: {response.status_code}, {response.json()}")
    if response.status_code == 404:
        return JSONResponse(
            status_code=404, 
            content={"detail": "Rider account not found. Please register at /riders/register"}
        )
    return JSONResponse(content=response.json(), status_code=response.status_code)

@rider_router.get("/gateway/riders")
async def gateway_get_riders():
    """
    Forwards a GET request to retrieve all riders from the Rider Service.
    """
    service_url = service["rider"]
    response = await forward_request(service_url, "GET", "/riders")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return JSONResponse(content=response.json(), status_code=response.status_code)



@rider_router.put("/gateway/riders/{rider_id}/availability")
async def gateway_update_availability(
    rider_id: int,
    availability: AvailabilityUpdate,      # We accept JSON { "is_available": true/false }
    token: str = Security(rider_oauth2_scheme),
    request: Request = None
):
    """
    API Gateway endpoint to update rider availability.
    1. Receives a JSON body: {"is_available": bool}
    2. Forwards 'is_available' as a query parameter to the Rider Service
       at /riders/{rider_id}/availability?is_available=...
    3. Attaches the Authorization header with the JWT token.
    """
    service_url = service["rider"]

    # Extract the boolean from the GatewayAvailability model
    is_available = availability.is_available

    # Build Authorization header
    headers = {"Authorization": f"Bearer {token}"}

    # The Rider Service expects ?is_available=someBool
    # and doesn't expect a JSON body. So we pass None for the body.
    url_path = f"/riders/{rider_id}/availability?is_available={is_available}"

    # Forward the request to the Rider Service
    response = await forward_request(
        service_url,
        "PUT",
        url_path,
        body=None,       # No JSON body, because Rider Service expects a query param
        headers=headers
    )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    # Return the Rider Service response as JSON
    return JSONResponse(content=response.json(), status_code=response.status_code)