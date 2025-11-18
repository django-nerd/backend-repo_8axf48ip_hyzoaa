"""
Database Schemas for Kinfash

Each Pydantic model represents a MongoDB collection. The collection name is the lowercase of the class name.

Use these models for validation in API endpoints. The database helper functions will insert timestamps automatically.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Literal
from datetime import datetime

# -----------------
# Core domain models
# -----------------

class Product(BaseModel):
    """
    Products collection schema
    Collection: "product"
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: Literal["men", "women", "unisex", "accessories"] = Field(..., description="Primary category")
    tags: List[str] = Field(default_factory=list, description="Additional tags like 'bestseller', 'new', 'limited'")
    images: List[str] = Field(default_factory=list, description="Image URLs")
    in_stock: bool = Field(True, description="Whether product is in stock")
    rating: float = Field(4.5, ge=0, le=5, description="Average rating")

class Drop(BaseModel):
    """
    Weekly or limited drops
    Collection: "drop"
    """
    title: str
    description: Optional[str] = None
    week_of: datetime = Field(default_factory=datetime.utcnow)
    items: List[str] = Field(default_factory=list, description="Product IDs referenced as strings")
    limited: bool = True
    banner: Optional[str] = Field(None, description="Banner image URL")

class Measurement(BaseModel):
    """
    Custom measurements stored per user/email
    Collection: "measurement"
    """
    email: EmailStr
    height_cm: Optional[float] = Field(None, ge=50, le=250)
    weight_kg: Optional[float] = Field(None, ge=20, le=300)
    chest_cm: Optional[float] = Field(None, ge=40, le=200)
    waist_cm: Optional[float] = Field(None, ge=40, le=200)
    hips_cm: Optional[float] = Field(None, ge=40, le=200)
    notes: Optional[str] = None

class QuizResult(BaseModel):
    """
    Style quiz results
    Collection: "quizresult"
    """
    email: Optional[EmailStr] = None
    style_vibe: Literal["minimal", "streetwear", "athleisure", "retro", "y2k", "preppy", "grunge"]
    color_pref: Literal["neon", "pastel", "monochrome", "earthy", "mixed"]
    budget: Literal["$", "$$", "$$$"]
    answers: List[str] = Field(default_factory=list)

class OrderItem(BaseModel):
    product_id: str
    qty: int = Field(ge=1)
    size: Optional[str] = None

class Order(BaseModel):
    """
    Simple order for quick checkout
    Collection: "order"
    """
    email: EmailStr
    items: List[OrderItem]
    subtotal: float = Field(ge=0)
    shipping: float = Field(ge=0, default=0)
    total: float = Field(ge=0)
    status: Literal["created", "paid", "shipped"] = "created"

# Optional user profile for personalization
class UserProfile(BaseModel):
    """
    User preferences & profile
    Collection: "userprofile"
    """
    email: EmailStr
    display_name: Optional[str] = None
    favorite_categories: List[str] = Field(default_factory=list)
    saved_items: List[str] = Field(default_factory=list)
    sustainability_pref: bool = False
