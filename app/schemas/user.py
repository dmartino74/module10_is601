from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

# ---------- NEWLY ADDED ----------
class UserCreate(BaseModel):
    """
    Schema for new user registration.
    This is used when a client sends data to create a new account.
    It includes the raw password, which will later be hashed before saving.
    """
    username: str
    email: EmailStr
    password: str

    # Example payload for API docs (Swagger/Redoc)
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "StrongPass123"
            }
        }
    )
# ---------- END OF NEW ADDITION ----------


class UserResponse(BaseModel):
    """
    Schema for user response data.
    This is what you return to the client after creating/fetching a user.
    Notice: no password field here, for security reasons.
    """
    id: UUID
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_verified: Optional[bool] = False
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Allows mapping directly from SQLAlchemy ORM objects
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """
    Schema for authentication token response.
    Returned after a successful login.
    """
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

    # Example payload for API docs
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                "token_type": "bearer",
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "username": "johndoe",
                    "email": "john.doe@example.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "is_active": True,
                    "is_verified": False,
                    "created_at": "2025-01-01T00:00:00",
                    "updated_at": "2025-01-08T12:00:00",
                },
            }
        }
    )


class TokenData(BaseModel):
    """
    Schema for JWT token payload.
    Used internally when decoding a JWT to extract the user_id.
    """
    user_id: Optional[UUID] = None


class UserLogin(BaseModel):
    """
    Schema for user login.
    This is the payload clients send to authenticate.
    """
    username: str
    password: str

    # Example payload for API docs
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "johndoe123",
                "password": "SecurePass123",
            }
        }
    )
