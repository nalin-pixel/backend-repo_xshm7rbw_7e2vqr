"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Fledge-specific schemas

class Lead(BaseModel):
    """Inbound project request (Start a Project)"""
    business_name: str = Field(..., description="Company or brand name")
    contact_name: str = Field(..., description="Primary contact full name")
    email: EmailStr
    phone: Optional[str] = Field(None, description="Contact phone number")
    project_type: str = Field(..., description="Type of project or service needed")
    budget: str = Field(..., description="Budget range")
    timeline: str = Field(..., description="Desired timeline")
    message: Optional[str] = Field(None, description="Additional context or goals")
    source: Optional[str] = Field("website", description="Lead source")

class Contact(BaseModel):
    """General contact form"""
    name: str
    email: EmailStr
    message: str
    phone: Optional[str] = None
    company: Optional[str] = None
    topic: Optional[str] = None

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
