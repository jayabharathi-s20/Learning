import pytest
from datetime import date, timedelta
from pydantic import ValidationError

from app.models import (
    UserCreate,
    CategoryCreate, 
    ItemCreate, ItemPatch
)


@pytest.fixture
def user_data():
    """Provide valid user data."""
    return {"name": "John", "email": "john@gmail.com"}


@pytest.fixture
def category_data():
    """Provide valid category data."""
    return {"name": "Medicine"}


@pytest.fixture
def item_data():
    """Provide valid item data."""
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
    """
    data = user_data
    user = UserCreate(**data)
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
    try:
        UserCreate(**data)
        assert False
    except ValidationError as e:
        assert "name" in str(e)


def test_user_short_name(user_data):
    """
    Test user creation with short name.

    Args:
        user_data (dict): Base user data.

    Raises:
        ValidationError: If name is too short.
    """
    data = user_data.copy()
    data["name"] = "J"
    try:
        UserCreate(**data)
        assert False
    except ValidationError as e:
        assert "name" in str(e)


def test_user_long_name(user_data):
    """
    Test user creation with long name.

    Args:
        user_data (dict): Base user data.

    Raises:
        ValidationError: If name is too long.
    """
    data = user_data.copy()
    data["name"] = "J" * 101
    try:
        UserCreate(**data)
        assert False
    except ValidationError as e:
        assert "name" in str(e)


def test_user_invalid_email(user_data):
    """
    Test user creation with invalid email.

    Args:
        user_data (dict): Base user data.

    Raises:
        ValidationError: If email is invalid.
    """
    data = user_data.copy()
    data["email"] = "invalid"
    try:
        UserCreate(**data)
        assert False
    except ValidationError as e:
        assert "email" in str(e)


def test_category_valid(category_data):
    """
    Test valid category creation.

    Args:
        category_data (dict): Valid category input.
    """
    data = category_data
    category = CategoryCreate(**data)
    assert category.name == "Medicine"


def test_category_empty(category_data):
    """
    Test category with empty name.

    Args:
        category_data (dict): Base category data.

    Raises:
        ValidationError: If name is empty.
    """
    data = category_data.copy()
    data["name"] = " "
    try:
        CategoryCreate(**data)
        assert False
    except ValidationError as e:
        assert "name" in str(e)


def test_category_short(category_data):
    """
    Test category with short name.

    Args:
        category_data (dict): Base category data.

    Raises:
        ValidationError: If name is too short.
    """
    data = category_data.copy()
    data["name"] = "A"
    try:
        CategoryCreate(**data)
        assert False
    except ValidationError as e:
        assert "name" in str(e)


def test_category_long(category_data):
    """
    Test category with long name.

    Args:
        category_data (dict): Base category data.

    Raises:
        ValidationError: If name is too long.
    """
    data = category_data.copy()
    data["name"] = "A" * 101
    try:
        CategoryCreate(**data)
        assert False
    except ValidationError as e:
        assert "name" in str(e)


def test_item_valid(item_data):
    """
    Test valid item creation.

    Args:
        item_data (dict): Valid item input.
    """
    data = item_data
    item = ItemCreate(**data)
    assert item.name == "Paracetamol"


def test_item_empty_name(item_data):
    """
    Test item with empty name.

    Args:
        item_data (dict): Base item data.

    Raises:
        ValidationError: If name is empty.
    """
    data = item_data.copy()
    data["name"] = " "
    try:
        ItemCreate(**data)
        assert False
    except ValidationError as e:
        assert "name" in str(e)


def test_item_negative_quantity(item_data):
    """
    Test item with negative quantity.

    Args:
        item_data (dict): Base item data.

    Raises:
        ValidationError: If quantity is negative.
    """
    data = item_data.copy()
    data["quantity"] = -1
    try:
        ItemCreate(**data)
        assert False
    except ValidationError as e:
        assert "quantity" in str(e)


def test_item_negative_threshold(item_data):
    """
    Test item with negative threshold.

    Args:
        item_data (dict): Base item data.

    Raises:
        ValidationError: If threshold is negative.
    """
    data = item_data.copy()
    data["threshold"] = -5
    try:
        ItemCreate(**data)
        assert False
    except ValidationError as e:
        assert "threshold" in str(e)


def test_item_invalid_price_zero(item_data):
    """
    Test item with zero price.

    Args:
        item_data (dict): Base item data.

    Raises:
        ValidationError: If price is zero.
    """
    data = item_data.copy()
    data["price"] = 0
    try:
        ItemCreate(**data)
        assert False
    except ValidationError as e:
        assert "price" in str(e)


def test_item_invalid_price_negative(item_data):
    """
    Test item with negative price.

    Args:
        item_data (dict): Base item data.

    Raises:
        ValidationError: If price is negative.
    """
    data = item_data.copy()
    data["price"] = -10
    try:
        ItemCreate(**data)
        assert False
    except ValidationError as e:
        assert "price" in str(e)


def test_item_past_expiry(item_data):
    """
    Test item with past expiry date.

    Args:
        item_data (dict): Base item data.

    Raises:
        ValidationError: If expiry date is in the past.
    """
    data = item_data.copy()
    data["expiry_date"] = date.today() - timedelta(days=1)
    try:
        ItemCreate(**data)
        assert False
    except ValidationError as e:
        assert "expiry_date" in str(e)


def test_item_patch_invalid_price():
    """
    Test patch with invalid price.

    Raises:
        ValidationError: If price is negative.
    """
    data = {"price": -10}
    try:
        ItemPatch(**data)
        assert False
    except ValidationError as e:
        assert "price" in str(e)
