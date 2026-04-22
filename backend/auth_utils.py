import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Define the secret key for JWT
SECRET_KEY = "secret_key_for_jwt"

# Define the JWT token expiration time in minutes
TOKEN_EXPIRE_MINUTES = 60

def create_jwt_token(user_id: int, username: str, email: str):
    """
    Create a JWT token for the given user.
    
    Args:
    user_id (int): The ID of the user.
    username (str): The username of the user.
    email (str): The email address of the user.
    
    Returns:
    str: The JWT token.
    """
    payload = {
        "sub": user_id,
        "name": username,
        "email": email,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def verify_jwt_token(token: str):
    """
    Verify the given JWT token.
    
    Args:
    token (str): The JWT token.
    
    Returns:
    dict: The payload of the JWT token if it is valid, otherwise None.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Define the JWT authentication scheme
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Get the current user from the JWT token in the Authorization header.
    
    Args:
    credentials (HTTPAuthorizationCredentials): The Authorization header.
    
    Returns:
    dict: The payload of the JWT token.
    """
    token = credentials.credentials
    payload = verify_jwt_token(token)
    return payload
