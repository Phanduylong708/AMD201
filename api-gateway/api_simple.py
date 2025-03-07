from dotenv import load_dotenv
from pathlib import Path
import os

# Load .env file from the current directory
env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)

from fastapi import FastAPI, Request, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
from datetime import timedelta
from src.service.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from src.error import APIGatewayError, AuthError

# Service URLs from environment variables (with defaults)
services = {
    "user": os.getenv("USER_SERVICE_URL", "http://localhost:8001"),
    "rider": os.getenv("RIDER_SERVICE_URL", "http://localhost:8002"),
    "booking": os.getenv("BOOKING_SERVICE_URL", "http://localhost:8004"),
    "ride_matching": os.getenv("RIDE_MATCHING_SERVICE_URL", "http://localhost:8003"),
}

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

async def forward_request(service_url: str, method: str, path: str, body=None, headers=None):
    """Forward a request to a service and return the response."""
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            request_kwargs = {
                "headers": headers or {}
            }
            
            if body is not None:
                request_kwargs["json"] = body
            
            print(f"Forwarding {method} request to {service_url}{path}")
            response = await client.request(
                method,
                f"{service_url}{path}",
                **request_kwargs
            )
            print(f"Received response with status code {response.status_code}")
            return response
    except httpx.TimeoutException:
        raise APIGatewayError.service_connection_error("service", "Timeout")
    except Exception as e:
        raise APIGatewayError.gateway_error(e)

@app.post("/gateway/login/{service}", tags=["Authentication"])
async def login(service: str, form_data: OAuth2PasswordRequestForm = Depends()):
    """Login endpoint that supports both users and riders."""
    if service not in ["user", "rider"]:
        raise APIGatewayError.service_not_found(service, ["user", "rider"])

    service_url = services[service]
    login_path = "/token" if service == "user" else "/riders/login"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{service_url}{login_path}",
                data={"username": form_data.username, "password": form_data.password},
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
        
        if response.status_code != 200:
            return AuthError.service_auth_error(response, service)

        # Create gateway token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": form_data.username, "role": service},
            expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
        
    except httpx.RequestError as e:
        raise APIGatewayError.service_connection_error(service, e)

@app.api_route("/gateway/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway(service: str, path: str, request: Request):
    """Dynamic gateway route that forwards requests to appropriate services."""
    if service not in services:
        raise APIGatewayError.service_not_found(service, list(services.keys()))
    
    service_url = services[service]
    
    # Get query parameters
    query_params = str(request.query_params) if request.query_params else ""
    
    # Get request body for methods that typically have one
    body = None
    if request.method in ["POST", "PUT", "PATCH"]:
        content_type = request.headers.get("content-type", "").lower()
        if "application/json" in content_type:
            try:
                body = await request.json()
            except Exception as e:
                raise APIGatewayError.invalid_json_body(e)
        elif "application/x-www-form-urlencoded" in content_type:
            form_data = await request.form()
            body = dict(form_data)
    
    # Forward any authorization header
    headers = {}
    if "Authorization" in request.headers:
        headers["Authorization"] = request.headers.get("Authorization")
    
    try:
        print(f"Gateway: Forwarding {request.method} request to {service} service, path: /{path}")
        # Add query params to path if they exist
        full_path = f"/{path}{'?' + query_params if query_params else ''}"
        response = await forward_request(service_url, request.method, full_path, body, headers)
        
        # Handle response using the error handler
        status_code, content = APIGatewayError.handle_service_response(response)
        return JSONResponse(status_code=status_code, content=content)
        
    except httpx.RequestError as e:
        raise APIGatewayError.service_connection_error(service, e)
    except Exception as e:
        raise APIGatewayError.gateway_error(e)

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting API Gateway...")
    print("📚 Swagger UI will be available at: http://localhost:8000/docs")
    print("🔄 ReDoc will be available at: http://localhost:8000/redoc")
    uvicorn.run("api_simple:app", host="0.0.0.0", port=8000, reload=True) 