from pydantic import BaseModel, validator
from typing import Optional

class UserRequest(BaseModel):
    username: str
    password: str
    email: str

    @validator("username")
    def validate_username(cls, value):
        if len(value) < 3 or len(value) > 20:
            raise ValueError("Username must be between 3 and 20 characters long")
        if not value.replace("_", "").isalnum():
            raise ValueError("Username can only contain letters, numbers, and underscores")
        return value

    @validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one number")
        return value

    @validator("email")
    def validate_email(cls, value):
        if "@" not in value:
            raise ValueError("Invalid email address")
        return value

class RepositoryRequest(BaseModel):
    name: str
    url: str

    @validator("name")
    def validate_name(cls, value):
        if len(value) < 3 or len(value) > 50:
            raise ValueError("Repository name must be between 3 and 50 characters long")
        if not value.replace("_", "").isalnum():
            raise ValueError("Repository name can only contain letters, numbers, and underscores")
        return value

    @validator("url")
    def validate_url(cls, value):
        if not value.startswith("http://") and not value.startswith("https://"):
            raise ValueError("Invalid repository URL")
        return value
