import os
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Union

from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import declarative_base, Session

from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import ValidationError

from app.schemas.user import UserCreate, UserResponse, Token

# SQLAlchemy base
Base = declarative_base()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Config (use env vars in production)
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class User(Base):
    __tablename__ = "users"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)

    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)

    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __init__(self, **kwargs):
        """Allow passing `password` directly into constructor for tests."""
        password = kwargs.pop("password", None)
        kwargs.pop("password_hash", None)
        super().__init__(**kwargs)
        if password is not None:
            # If already looks like a bcrypt hash, store directly
            if password.startswith("$2b$") or password.startswith("$2a$"):
                self.password_hash = password
            else:
                self.password = password  # triggers hashing

    def __repr__(self):
        # Prefer full name if present
        if self.first_name and self.last_name:
            return f"<User(name={self.first_name} {self.last_name}, email={self.email})>"
        elif self.first_name:
            return f"<User(name={self.first_name}, email={self.email})>"
        return f"<User(name={self.username}, email={self.email})>"

    # -------------------------
    # Password property & utils
    # -------------------------
    @property
    def password(self):
        raise AttributeError("Password is write-only")

    @password.setter
    def password(self, plaintext: str):
        self.password_hash = self.hash_password(plaintext)

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password_hash)

    # -------------------------
    # JWT utilities
    # -------------------------
    @staticmethod
    def create_access_token_for_username(identifier: Union[str, uuid.UUID], expires_delta: Optional[timedelta] = None) -> str:
        """Create a token with either the user's UUID or username as subject."""
        to_encode = {"sub": str(identifier)}
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Alias expected by tests: accepts arbitrary dict"""
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def verify_token(token: str) -> Optional[Union[uuid.UUID, str]]:
        """
        Return the UUID object if sub is a valid UUID string,
        otherwise return the raw string (e.g., username).
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            sub = payload.get("sub")
            if not sub:
                return None
            try:
                return uuid.UUID(sub)
            except (ValueError, TypeError):
                return sub
        except JWTError:
            return None

    # -------------------------
    # Business logic
    # -------------------------
    @classmethod
    def register(cls, db: Session, user_data: Dict[str, Any]) -> "User":
        try:
            user_create = UserCreate.model_validate(user_data)

            if not user_create.password or len(user_create.password) < 6:
                raise ValueError("Password must be at least 6 characters long")

            existing = db.query(cls).filter(
                (cls.email == user_create.email) | (cls.username == user_create.username)
            ).first()
            if existing:
                raise ValueError("Username or email already exists")

            new_user = cls(
                username=user_create.username,
                email=user_create.email,
                first_name=user_create.first_name,
                last_name=user_create.last_name,
                password=user_create.password,
            )

            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user

        except ValidationError as e:
            if "password" in str(e):
                raise ValueError("Password must be at least 6 characters long")
            raise ValueError(str(e))

    @classmethod
    def authenticate(cls, db: Session, username_or_email: str, password: str) -> Optional[dict]:
        user = db.query(cls).filter(
            (cls.username == username_or_email) | (cls.email == username_or_email)
        ).first()

        if not user or not user.verify_password(password):
            return None

        user.last_login = datetime.utcnow()
        db.commit()

        user_response = UserResponse.model_validate(user)
        token_response = Token(
            access_token=cls.create_access_token_for_username(user.id),
            token_type="bearer",
            user=user_response,
        )
        return token_response.model_dump()
