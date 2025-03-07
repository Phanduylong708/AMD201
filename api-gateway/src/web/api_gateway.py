from fastapi import APIRouter, HTTPException, Depends, Security, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from src.model.rider import AvailabilityUpdate
import httpx
import os
from datetime import timedelta, datetime
from src.service.security import (
    create_access_token,
    get_current_user,
    get_current_rider,
    get_current_admin,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    oauth2_scheme,
    rider_oauth2_scheme,
    SECRET_KEY,
    ALGORITHM
)
from jose import jwt


# Service URLs from environment variables (with defaults)
service = {
    "user": os.getenv("USER_SERVICE_URL", "http://localhost:8001"),
    "rider": os.getenv("RIDER_SERVICE_URL", "http://localhost:8002"),
    "booking": os.getenv("BOOKING_SERVICE_URL", "http://localhost:8003"),
    "ride_matching": os.getenv("RIDE_MATCHING_SERVICE_URL", "http://localhost:8004"),
}

rider_router = APIRouter()
user_router = APIRouter()


async def forward_request(service_url: str, method: str, path: str, body=None, headers=None):
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method,
            f"{service_url}{path}",
            json=body,
            headers=headers
        )
        return response


# User Service Routes
@user_router.post("/gateway/login/user")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    API Gateway login endpoint for Users.
    Forwards the login request to the User Service and creates a gateway JWT token.
    """
    service_url = service["user"]
    print(f"🔍 Forwarding user login request to {service_url}/token")

    login_data = {"username": form_data.username, "password": form_data.password}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{service_url}/token",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

    if response.status_code != 200:
        if response.status_code == 404:
            return JSONResponse(
                status_code=404,
                content={"detail": "User account not found. Please register first."}
            )
        return JSONResponse(content=response.json(), status_code=response.status_code)

    # Create a new gateway token with role="user"
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username, "role": "user"},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@user_router.post("/gateway/users")
async def create_user(request: Request):
    """Forward user registration request to User Service."""
    body = await request.json()
    response = await forward_request(service["user"], "POST", "/users", body)
    return JSONResponse(content=response.json(), status_code=response.status_code)

@user_router.get("/gateway/users/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Forward request to get current user's profile."""
    response = await forward_request(
        service["user"],
        "GET",
        f"/users/me",
        headers={"Authorization": f"Bearer {current_user['username']}"}
    )
    return JSONResponse(content=response.json(), status_code=response.status_code)

@user_router.put("/gateway/users/me")
async def update_current_user_info(request: Request, current_user: dict = Depends(get_current_user)):
    """Forward request to update current user's profile."""
    body = await request.json()
    response = await forward_request(
        service["user"],
        "PUT",
        f"/users/me",
        body=body,
        headers={"Authorization": f"Bearer {current_user['username']}"}
    )
    return JSONResponse(content=response.json(), status_code=response.status_code)

@user_router.delete("/gateway/users/me")
async def delete_current_user_account(current_user: dict = Depends(get_current_user)):
    """Forward request to delete current user's account."""
    response = await forward_request(
        service["user"],
        "DELETE",
        f"/users/me",
        headers={"Authorization": f"Bearer {current_user['username']}"}
    )
    return JSONResponse(content=response.json(), status_code=response.status_code)

@user_router.get("/gateway/auth/status")
async def check_auth_status(current_user: dict = Depends(get_current_user)):
    """Check authentication status."""
    return {
        "message": "Authentication valid",
        "username": current_user["username"],
        "role": current_user["role"]
    }

@user_router.get("/gateway/token/decode")
async def decode_token(token: str = Depends(oauth2_scheme)):
    """
    Decode and return the information stored in the JWT token.
    This is useful for debugging and checking token contents.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expiration = datetime.fromtimestamp(payload["exp"])
        remaining = (expiration - datetime.utcnow()).total_seconds()
        
        return {
            "username": payload["sub"],
            "role": payload["role"],
            "expiration": expiration.isoformat(),
            "remaining_seconds": remaining,
            "is_expired": remaining <= 0
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not decode token"
        )

# Rider Routes
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

    # Create a new gateway token with role="rider"
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username, "role": "rider"},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@rider_router.get("/gateway/riders")
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
    Requires rider authentication.
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