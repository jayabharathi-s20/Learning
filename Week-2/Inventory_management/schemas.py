from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import date

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
    pass


class UserUpdate(UserBase):
    """
    Schema for fully updating a user.
    """
    pass


class UserPatch(BaseModel):
    """
    Schema for partially updating a user.

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