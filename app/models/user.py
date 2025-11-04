# app/models/user.py

import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, Session

from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import ValidationError

from app.schemas.user import UserCreate, UserResponse, Token

# SQLAlchemy base
Base = declarative_base()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Config (move to environment variables in production!)
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"

    # -------------------------
    # Password utilities
    # -------------------------
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password_hash)

    # -------------------------
    # JWT utilities
    # -------------------------
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def verify_token(token: str) -> Optional[uuid.UUID]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")
            return uuid.UUID(user_id) if user_id else None
        except (JWTError, ValueError):
            return None

    # -------------------------
    # Business logic
    # -------------------------
    @classmethod
    def register(cls, db: Session, user_data: Dict[str, Any]) -> "User":
        """Register a new user with validation and hashing."""
        try:
            # Validate with Pydantic schema
            user_create = UserCreate.model_validate(user_data)

            # Check uniqueness
            existing = db.query(cls).filter(
                (cls.email == user_create.email) | (cls.username == user_create.username)
            ).first()
            if existing:
                raise ValueError("Username or email already exists")

            # Create new user
            new_user = cls(
                first_name=user_create.first_name,
                last_name=user_create.last_name,
                email=user_create.email,
                username=user_create.username,
                password_hash=cls.hash_password(user_create.password),
            )

            db.add(new_user)
            db.flush()
            return new_user

        except ValidationError as e:
            raise ValueError(str(e))

    @classmethod
    def authenticate(cls, db: Session, username_or_email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user and return token with user data."""
        user = db.query(cls).filter(
            (cls.username == username_or_email) | (cls.email == username_or_email)
        ).first()

        if not user or not user.verify_password(password):
            return None

        user.last_login = datetime.utcnow()
        db.commit()

        # Build token response
        user_response = UserResponse.model_validate(user)
        token_response = Token(
            access_token=cls.create_access_token({"sub": str(user.id)}),
            token_type="bearer",
            user=user_response,
        )
        return token_response.model_dump()
