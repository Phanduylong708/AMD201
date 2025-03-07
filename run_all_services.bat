@echo off
echo Launching all services...
start cmd /k "python services/rider/main.py"
start cmd /k "python services/booking/main.py"
start cmd /k "python services/ride_matching/main.py"
start cmd /k "python services/user/main.py"
start cmd /k "python api-gateway/api_simple.py"
echo All services launched. Press any key to exit.
pause >nul 