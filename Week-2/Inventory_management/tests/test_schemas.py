import pytest
from datetime import date, timedelta
from pydantic import ValidationError

from Inventory_management.schemas import (
    UserCreate, UserPatch,
    CategoryCreate, CategoryPatch,
    ItemCreate, ItemPatch
)

def test_user_valid():
    user = UserCreate(name="John", email="john@gmail.com")
    assert user.name == "John"


def test_user_empty_name():
    with pytest.raises(ValidationError):
        UserCreate(name=" ", email="john@gmail.com")


def test_user_short_name():
    with pytest.raises(ValidationError):
        UserCreate(name="J", email="john@gmail.com")


def test_user_long_name():
    with pytest.raises(ValidationError):
        UserCreate(name="J" * 101, email="john@gmail.com")


def test_user_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(name="John", email="invalid")


def test_user_patch_optional():
    user = UserPatch()
    assert user.name is None


def test_category_valid():
    category = CategoryCreate(name="Medicine")
    assert category.name == "Medicine"


def test_category_empty():
    with pytest.raises(ValidationError):
        CategoryCreate(name=" ")


def test_category_short():
    with pytest.raises(ValidationError):
        CategoryCreate(name="A")


def test_category_long():
    with pytest.raises(ValidationError):
        CategoryCreate(name="A" * 101)


def test_category_patch_optional():
    cat = CategoryPatch()
    assert cat.name is None


def valid_item_data():
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


def test_item_valid():
    item = ItemCreate(**valid_item_data())
    assert item.name == "Paracetamol"


def test_item_empty_name():
    data = valid_item_data()
    data["name"] = " "
    with pytest.raises(ValidationError):
        ItemCreate(**data)


def test_item_negative_quantity():
    data = valid_item_data()
    data["quantity"] = -1
    with pytest.raises(ValidationError):
        ItemCreate(**data)


def test_item_negative_threshold():
    data = valid_item_data()
    data["threshold"] = -5
    with pytest.raises(ValidationError):
        ItemCreate(**data)


def test_item_invalid_price_zero():
    data = valid_item_data()
    data["price"] = 0
    with pytest.raises(ValidationError):
        ItemCreate(**data)


def test_item_invalid_price_negative():
    data = valid_item_data()
    data["price"] = -10
    with pytest.raises(ValidationError):
        ItemCreate(**data)


def test_item_past_expiry():
    data = valid_item_data()
    data["expiry_date"] = date.today() - timedelta(days=1)
    with pytest.raises(ValidationError):
        ItemCreate(**data)


def test_item_patch_partial():
    item = ItemPatch(name="Updated")
    assert item.name == "Updated"
    assert item.quantity is None


def test_item_patch_invalid_price():
    with pytest.raises(ValidationError):
        ItemPatch(price=-10)