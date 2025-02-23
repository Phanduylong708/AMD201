from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
import httpx
import uvicorn
from src.model.schemas import LoginRequest  # ✅ Import the Pydantic model

# Define services
service = {
    "user": "http://localhost:8001",
    "rider": "http://localhost:8002"
}

app = FastAPI()

async def forward_request(service_url: str, method: str, path: str, body=None, headers=None):
    """
    Handles forwarding API requests to the appropriate microservice.
    """
    async with httpx.AsyncClient() as client:
        response = await client.request(method, f"{service_url}{path}", json=body, headers=headers)
        return response

# ✅ **User Login (Accepts username & password)**
@app.post("/gateway/login/user")
async def login_user(login_data: LoginRequest):  # ✅ Use Pydantic model
    """
    API Gateway login endpoint for Users.
    """
    service_url = service["user"]
    response = await forward_request(service_url, "POST", "/login", login_data.dict(), None)

    # ✅ Handle case where user does not exist
    if response.status_code == 404:
        return JSONResponse(
            status_code=404, 
            content={"detail": "User account not found. Please register at /users/register"}
        )

    return JSONResponse(content=response.json(), status_code=response.status_code)

# ✅ **Rider Login (Accepts username & password)**
@app.post("/gateway/login/rider")
async def login_rider(login_data: LoginRequest):  # ✅ Use Pydantic model
    """
    API Gateway login endpoint for Riders.
    """
    service_url = service["rider"]
    response = await forward_request(service_url, "POST", "/login", login_data.dict(), None)

    #Handle case where rider does not exist
    if response.status_code == 404:
        return JSONResponse(
            status_code=404, 
            content={"detail": "Rider account not found. Please register at /riders/register"}
        )

    return JSONResponse(content=response.json(), status_code=response.status_code)

if __name__ == "__main__":
    uvicorn.run("api:app", reload=True, host="0.0.0.0", port=8000)
