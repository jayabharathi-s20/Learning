from app.database import Base
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import date

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    role = Column(String,nullable=True) 
    items = relationship( "Item", back_populates="owner")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    items = relationship("Item", back_populates="category", cascade="all", passive_deletes=True)

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, default=0)
    threshold = Column(Integer, default=0)
    price = Column(Float, default=0.0)
    supplier = Column(String)
    expiry_date = Column(Date)
    category_id = Column(Integer,ForeignKey("categories.id", ondelete="CASCADE"),nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = relationship("Category", back_populates="items")
    owner = relationship("User", back_populates="items")



def validate_name_common(value: str, field_name: str = "Field"):
    value = value.strip()

    if not value:
        raise ValueError(f"{field_name} cannot be empty")

    if len(value) < 2:
        raise ValueError(f"{field_name} must be at least 2 characters")

    if len(value) > 100:
        raise ValueError(f"{field_name} must not exceed 100 characters")

    return value


class UserBase(BaseModel):
    """
    Base schema for User.

    Attributes:
        name (str): Name of the user
        email (EmailStr): Email address of the user
    """
    name: str
    email: EmailStr

    @field_validator("name")
    def validate_name(cls, value):
        return validate_name_common(value, "Name")


class UserCreate(UserBase):
    """
    Schema for creating a user.
    """
    password: str
    role: Optional[str] = None

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters")
        if len(value) > 128:
            raise ValueError("Password too long")
        return value

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    def validate_password(cls, value):
        if not value or value.strip() == "":
            raise ValueError("Password cannot be empty")
        return value
    
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserUpdate(UserBase):
    """
    Schema for fully updating a user.
    """
    pass


class UserPatch(BaseModel):
    """
    Schema for partially updating a user.
        raise ValueError("Password must be at least 6 characters")

    All fields are optional.
    """
    name: Optional[str] = None
    email: Optional[EmailStr] = None

    @field_validator("name")
    def validate_name(cls, value):
        return validate_name_common(value, "Name")



class CategoryBase(BaseModel):
    """
    Base schema for Category.

    Attributes:
        name (str): Category name
    """
    name: str
    

    @field_validator("name")
    def validate_name(cls, value):
        return validate_name_common(value, "Name")


class CategoryCreate(CategoryBase):
    """
    Schema for creating a category.
    """
    pass


class CategoryUpdate(CategoryBase):
    """
    Schema for fully updating a category.
    """
    pass


class CategoryPatch(BaseModel):
    """
    Schema for partially updating a category.
    """
    name: Optional[str] = None

    @field_validator("name")
    def validate_name(cls, value):
        return validate_name_common(value, "Name")



class ItemBase(BaseModel):
    """
    Base schema for Item.

    Attributes:
        name (str): Item name
        quantity (int): Available quantity
        threshold (int): Minimum stock threshold
        price (float): Price of item
        supplier (str): Supplier name
        expiry_date (date): Expiry date
        category_id (int): Category ID
        created_by (int): User ID
    """
    name: str
    quantity: int
    threshold: int
    price: float
    supplier: str
    expiry_date: date
    category_id: int
    created_by: int

    @field_validator("name")
    def validate_name(cls, value):
        return validate_name_common(value, "Name")

    @field_validator("quantity", "threshold")
    def validate_numbers(cls, value):
        """
        Validate numeric fields (quantity, threshold).
        """
        if value < 0:
            raise ValueError("Value cannot be negative")
        return value

    @field_validator("price")
    def validate_price(cls, value):
        """
        Validate price field.
        """
        if value <= 0:
            raise ValueError("Price must be greater than 0")
        return value

    @field_validator("expiry_date")
    def validate_expiry(cls, value):
        """
        Validate expiry date.

        Rule:
            - Cannot be in the past
        """
        if value < date.today():
            raise ValueError("Expiry date cannot be in the past")
        return value


class ItemCreate(ItemBase):
    """
    Schema for creating an item.
    """
    pass


class ItemUpdate(ItemBase):
    """
    Schema for fully updating an item.
    """
    pass


class ItemPatch(BaseModel):
    """
    Schema for partially updating an item.

    All fields are optional.
    """
    name: Optional[str] = None
    quantity: Optional[int] = None
    threshold: Optional[int] = None
    price: Optional[float] = None
    supplier: Optional[str] = None
    expiry_date: Optional[date] = None
    category_id: Optional[int] = None
    created_by: Optional[int] = None

    @field_validator("name")
    def validate_name(cls, value):
        return validate_name_common(value, "Name")

    @field_validator("quantity", "threshold")
    def validate_numbers(cls, value):
        """
        Validate numeric fields if provided.
        """
        if value is not None and value < 0:
            raise ValueError("Value cannot be negative")
        return value

    @field_validator("price")
    def validate_price(cls, value):
        """
        Validate price if provided.
        """
        if value is not None and value <= 0:
            raise ValueError("Price must be greater than 0")
        return value

    @field_validator("expiry_date")
    def validate_expiry(cls, value):
        """
        Validate expiry date if provided.
        """
        if value is not None and value < date.today():
            raise ValueError("Expiry date cannot be in the past")
        return value