from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID



class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str | None = None
    last_name: str | None = None


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool

    created_at: datetime
    modified_at: datetime | None = None
    deleted_at: datetime | None = None

    class Config:
        from_attributes = True