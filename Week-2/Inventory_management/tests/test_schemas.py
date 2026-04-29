import pytest
from datetime import date, timedelta
from pydantic import ValidationError

from Inventory_management.schemas import (
    UserCreate,
    CategoryCreate, 
    ItemCreate, ItemPatch
)


@pytest.fixture
def user_data():
    """
    Returns:
        dict: Valid user data with name and email.
    """
    return {
        "name": "John",
        "email": "john@gmail.com"
    }


@pytest.fixture
def category_data():
    """
    Returns:
        dict: Valid category data.
    """
    return {
        "name": "Medicine"
    }


@pytest.fixture
def item_data():
    """
    Returns:
        dict: Valid item data including quantity, price, expiry, etc.
    """
    return {
        "name": "Paracetamol",
        "quantity": 10,
        "threshold": 2,
        "price": 50.0,
        "supplier": "ABC Pharma",
        "expiry_date": date.today() + timedelta(days=10),
        "category_id": 1,
        "created_by": 1
    }



def test_user_valid(user_data):
    """
    Test creating a valid user.

    Args:
        user_data (dict): Valid user input.

    Returns:
        None

    Raises:
        AssertionError: If user creation fails.
    """
    user = UserCreate(**user_data)
    assert user.name == "John"


def test_user_empty_name(user_data):
    """
    Test user creation with empty name.

    Args:
        user_data (dict): Base user data.

    Raises:
        ValidationError: If name is empty.
    """
    data = user_data.copy()
    data["name"] = " "

    with pytest.raises(ValidationError):
        UserCreate(**data)


def test_user_short_name(user_data):
    """
    Test user creation with too short name.

    Raises:
        ValidationError: If name length is below minimum.
    """
    data = user_data.copy()
    data["name"] = "J"

    with pytest.raises(ValidationError):
        UserCreate(**data)


def test_user_long_name(user_data):
    """
    Test user creation with too long name.

    Raises:
        ValidationError: If name exceeds max length.
    """
    data = user_data.copy()
    data["name"] = "J" * 101

    with pytest.raises(ValidationError):
        UserCreate(**data)


def test_user_invalid_email(user_data):
    """
    Test user creation with invalid email format.

    Raises:
        ValidationError: If email format is invalid.
    """
    data = user_data.copy()
    data["email"] = "invalid"

    with pytest.raises(ValidationError):
        UserCreate(**data)


def test_category_valid(category_data):
    """
    Test valid category creation.

    Args:
        category_data (dict): Valid category input.
    """
    category = CategoryCreate(**category_data)
    assert category.name == "Medicine"


def test_category_empty(category_data):
    """
    Test category with empty name.

    Raises:
        ValidationError: If name is empty.
    """
    data = category_data.copy()
    data["name"] = " "

    with pytest.raises(ValidationError):
        CategoryCreate(**data)


def test_category_short(category_data):
    """
    Test category with short name.

    Raises:
        ValidationError: If name is too short.
    """
    data = category_data.copy()
    data["name"] = "A"

    with pytest.raises(ValidationError):
        CategoryCreate(**data)


def test_category_long(category_data):
    """
    Test category with long name.

    Raises:
        ValidationError: If name exceeds max length.
    """
    data = category_data.copy()
    data["name"] = "A" * 101

    with pytest.raises(ValidationError):
        CategoryCreate(**data)



def test_item_valid(item_data):
    """
    Test valid item creation.

    Args:
        item_data (dict): Valid item input.
    """
    item = ItemCreate(**item_data)
    assert item.name == "Paracetamol"


def test_item_empty_name(item_data):
    """
    Test item with empty name.

    Raises:
        ValidationError: If name is empty.
    """
    data = item_data.copy()
    data["name"] = " "

    with pytest.raises(ValidationError):
        ItemCreate(**data)


def test_item_negative_quantity(item_data):
    """
    Test item with negative quantity.

    Raises:
        ValidationError: If quantity is negative.
    """
    data = item_data.copy()
    data["quantity"] = -1

    with pytest.raises(ValidationError):
        ItemCreate(**data)


def test_item_negative_threshold(item_data):
    """
    Test item with negative threshold.

    Raises:
        ValidationError: If threshold is negative.
    """
    data = item_data.copy()
    data["threshold"] = -5

    with pytest.raises(ValidationError):
        ItemCreate(**data)


def test_item_invalid_price_zero(item_data):
    """
    Test item with zero price.

    Raises:
        ValidationError: If price is zero.
    """
    data = item_data.copy()
    data["price"] = 0

    with pytest.raises(ValidationError):
        ItemCreate(**data)


def test_item_invalid_price_negative(item_data):
    """
    Test item with negative price.

    Raises:
        ValidationError: If price is negative.
    """
    data = item_data.copy()
    data["price"] = -10

    with pytest.raises(ValidationError):
        ItemCreate(**data)


def test_item_past_expiry(item_data):
    """
    Test item with past expiry date.

    Raises:
        ValidationError: If expiry date is in the past.
    """
    data = item_data.copy()
    data["expiry_date"] = date.today() - timedelta(days=1)

    with pytest.raises(ValidationError):
        ItemCreate(**data)


def test_item_patch_invalid_price():
    """
    Test patching item with invalid price.

    Raises:
        ValidationError: If price is negative.
    """
    with pytest.raises(ValidationError):
        ItemPatch(price=-10)