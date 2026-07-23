from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from pydantic import field_validator
import re

# ============================================
# CATEGORY MODEL
# ============================================

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True, min_length=2, max_length=50)
    description: Optional[str] = Field(default=None, max_length=200)
    products: List["Product"] = Relationship(back_populates="category")

# ============================================
# PRODUCT MODEL
# ============================================

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, min_length=2, max_length=100)
    description: str = Field(min_length=10, max_length=500)
    price: float = Field(gt=0)
    stock: int = Field(ge=0, default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    category: Optional[Category] = Relationship(back_populates="products")

# ============================================
# PRODUCT CREATE MODEL (WITH VALIDATION)
# ============================================

class ProductCreate(SQLModel):
    name: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=10, max_length=500)
    price: float = Field(gt=0, le=1000000)
    stock: int = Field(ge=0, le=100000)
    category_id: Optional[int] = None

    # VALIDATION: Name must start with capital letter
    @field_validator("name")
    def validate_name(cls, v):
        if not v[0].isupper():
            raise ValueError("Name must start with a capital letter")
        if re.search(r'[^a-zA-Z0-9\s\-]', v):
            raise ValueError("Name cannot contain special characters (only letters, numbers, spaces, and hyphens allowed)")
        return v

    # VALIDATION: Price must be at least 1 and rounded to 2 decimals
    @field_validator("price")
    def validate_price(cls, v):
        if v < 1:
            raise ValueError("Price must be at least 1")
        return round(v, 2)

    # VALIDATION: Stock cannot be negative
    @field_validator("stock")
    def validate_stock(cls, v):
        if v < 0:
            raise ValueError("Stock cannot be negative")
        return v

# ============================================
# PRODUCT UPDATE MODEL
# ============================================

class ProductUpdate(SQLModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, min_length=10, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)

# ============================================
# CATEGORY CREATE MODEL
# ============================================

class CategoryCreate(SQLModel):
    name: str = Field(min_length=2, max_length=50)
    description: Optional[str] = Field(None, max_length=200)