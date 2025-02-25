from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from src.service.security import create_access_token, authenticate_rider, authenticate_user

router = APIRouter()

@router.post("/users/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": user.username, "role": "user"})
    
    return JSONResponse(
        content={"access_token": access_token, "token_type": "bearer", "redirect": "http://localhost:8001/dashboard"},
        status_code=200
    )



@router.post("/riders/login")
def login_rider(form_data: OAuth2PasswordRequestForm = Depends()):
    rider = authenticate_rider(form_data.username, form_data.password)
    if not rider:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": rider.username, "role": "rider"})
    
    return JSONResponse(
        content={"access_token": access_token, "token_type": "bearer", "redirect": "http://localhost:8002/docs#"},
        status_code=200
    )
