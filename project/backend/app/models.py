from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str = ""


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class SweetBase(BaseModel):
    name: str = Field(..., min_length=1)
    description: str = ""
    category: str = Field(..., min_length=1)
    price: Decimal = Field(..., ge=0)
    quantity: int = Field(..., ge=0)
    image_url: str = ""


class SweetCreate(SweetBase):
    pass


class SweetUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[Decimal] = None
    quantity: Optional[int] = None
    image_url: Optional[str] = None


class SweetResponse(SweetBase):
    id: str
    created_at: datetime
    updated_at: datetime


class PurchaseRequest(BaseModel):
    quantity: int = Field(..., gt=0)


class RestockRequest(BaseModel):
    quantity: int = Field(..., gt=0)


class PurchaseResponse(BaseModel):
    id: str
    user_id: str
    sweet_id: str
    quantity: int
    total_price: Decimal
    purchased_at: datetime


class SearchParams(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None
