from typing import Optional
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx
from src.model import user, rider
from src.data.init import create_tables
from fastapi.middleware.cors import CORSMiddleware

service = {
    "creature": "http://localhost:8001",
    "explorer": "http://localhost:8002",
}

origins = ["*"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["+"],
    allow_headers=["+"],
)

async def forward_request(service_url: str, method: str, path: str, body=None, headers=None):
    async with httpx.AsyncClient() as client:
        response = await client.request(method, f"{service_url}{path}", json=body, headers=headers)
        return response

@app.api_route("/gateway/{service}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"], tags=["ApiGateway"])
async def gateway(request: Request, services: str, parameter: Optional[str] = ""):
    service_url = services[service]
    if service not in services:
        raise HTTPException(status_code=404, detail="Service not found")
    
    body = await request.json() if request.method in ["POST", "PUT", "PATCH"] else None

    response = await forward_request(service_url, request.method, f"/{service}/{parameter}", body, None)
    
    return JSONResponse(content=response.json(), status_code=response.status_code)

if __name__ == "__main__":
    create_tables()
    uvicorn.run("api:app", reload=True, host="0.0.0.0", port=8003)