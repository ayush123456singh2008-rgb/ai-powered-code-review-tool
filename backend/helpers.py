from fastapi import Response
from fastapi.responses import JSONResponse

def format_response(status_code: int, message: str, data: Optional[dict] = None):
    """
    Format the response as a JSON object.
    
    Args:
    status_code (int): The status code of the response.
    message (str): The message of the response.
    data (Optional[dict]): The data of the response.
    
    Returns:
    Response: The formatted response.
    """
    response = {
        "status_code": status_code,
        "message": message
    }
    if data:
        response["data"] = data
    return JSONResponse(content=response, status_code=status_code)

def handle_exception(status_code: int, message: str):
    """
    Handle an exception by returning a formatted response.
    
    Args:
    status_code (int): The status code of the response.
    message (str): The message of the response.
    
    Returns:
    Response: The formatted response.
    """
    return format_response(status_code, message)