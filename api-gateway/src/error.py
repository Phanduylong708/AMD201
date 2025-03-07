from fastapi import HTTPException
from fastapi.responses import JSONResponse
import httpx


class APIGatewayError:
    @staticmethod
    def service_not_found(service: str, available_services: list) -> HTTPException:
        """Raise when requested service is not found"""
        return HTTPException(
            status_code=404, 
            detail=f"Service '{service}' not found. Available services: {available_services}"
        )

    @staticmethod
    def invalid_json_body(error: Exception) -> HTTPException:
        """Raise when request body is not valid JSON"""
        return HTTPException(
            status_code=400, 
            detail=f"Invalid JSON body: {str(error)}"
        )

    @staticmethod
    def service_connection_error(service: str, error: Exception) -> HTTPException:
        """Raise when connection to service fails"""
        return HTTPException(
            status_code=503, 
            detail=f"Could not connect to {service} service: {str(error)}"
        )

    @staticmethod
    def gateway_error(error: Exception) -> HTTPException:
        """Raise for general gateway errors"""
        return HTTPException(
            status_code=500, 
            detail=f"Gateway error: {str(error)}"
        )

    @staticmethod
    def handle_service_response(response: httpx.Response) -> tuple[int, dict]:
        """Handle service response and return appropriate status code and content"""
        try:
            if response.status_code >= 400:
                error_detail = "Unknown error"
                try:
                    error_response = response.json()
                    error_detail = error_response.get("detail", str(error_response))
                except:
                    try:
                        error_detail = response.text
                    except:
                        error_detail = f"HTTP Error {response.status_code}"
                
                raise HTTPException(status_code=response.status_code, detail=error_detail)
            
            if response.status_code == 204:
                return 204, None
            
            return response.status_code, response.json()
        except ValueError:
            # If JSON parsing fails, return the raw text
            return response.status_code, {
                "result": response.text,
                "warning": "Non-JSON response received from service"
            }

class AuthError:
    @staticmethod
    def invalid_credentials(service: str) -> JSONResponse:
        """Return response for invalid credentials"""
        return JSONResponse(
            status_code=401,
            content={"detail": f"{service.title()} account not found or invalid credentials"}
        )

    @staticmethod
    def service_auth_error(response: httpx.Response, service: str) -> JSONResponse:
        """Handle authentication service error response"""
        error_detail = f"{service.title()} account not found or invalid credentials"
        try:
            error_response = response.json()
            if "detail" in error_response:
                error_detail = error_response["detail"]
        except:
            pass
            
        return JSONResponse(
            status_code=response.status_code,
            content={"detail": error_detail}
        )
