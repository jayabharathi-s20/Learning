import pytest
from Inventory_management import crud
from Inventory_management.models import User, Category,Item
from datetime import date, timedelta



def test_create_user(db):
    user = crud.create_user(db, {
        "name": "John",
        "email": "john@test.com"
    })

    assert user.id is not None
    assert user.email == "john@test.com"


def test_create_user_duplicate_email(db):
    crud.create_user(db, {"name": "John", "email": "dup@test.com"})

    with pytest.raises(ValueError):
        crud.create_user(db, {"name": "Jane", "email": "dup@test.com"})


def test_get_user(db):
    user = crud.create_user(db, {"name": "John", "email": "john@test.com"})

    fetched = crud.get_user(db, user.id)
    assert fetched.name == "John"


def test_update_user(db):
    user = crud.create_user(db, {"name": "John", "email": "john@test.com"})

    updated = crud.update_user(db, user.id, {"name": "Updated"})
    assert updated.name == "Updated"


def test_delete_user(db):
    user = crud.create_user(db, {"name": "John", "email": "john@test.com"})

    res = crud.delete_user(db, user.id)
    assert res["message"] == "User deleted"



def test_create_category(db):
    category = crud.create_category(db, {"name": "Medicine"})
    assert category.id is not None


def test_duplicate_category(db):
    crud.create_category(db, {"name": "Medicine"})

    with pytest.raises(ValueError):
        crud.create_category(db, {"name": "Medicine"})


def test_update_category(db):
    category = crud.create_category(db, {"name": "Old"})

    updated = crud.update_category(db, category.id, {"name": "New"})
    assert updated.name == "New"


def test_delete_category(db):
    category = crud.create_category(db, {"name": "Temp"})

    res = crud.delete_category(db, category.id)
    assert res["message"] == "Category deleted"



def setup_user_category(db):
    user = crud.create_user(db, {"name": "John", "email": "john@test.com"})
    category = crud.create_category(db, {"name": "Medicine"})
    return user, category


def test_create_item(db):
    user, category = setup_user_category(db)

    item = crud.create_item(db, {
        "name": "Paracetamol",
        "quantity": 10,
        "threshold": 2,
        "price": 50.0,
        "supplier": "ABC",
        "expiry_date": date.today() + timedelta(days=5),
        "category_id": category.id,
        "created_by": user.id
    })

    assert item.id is not None


def test_create_item_invalid_category(db):
    user = crud.create_user(db, {"name": "John", "email": "john@test.com"})

    with pytest.raises(ValueError):
        crud.create_item(db, {
            "name": "Item",
            "quantity": 10,
            "threshold": 2,
            "price": 50.0,
            "supplier": "ABC",
            "expiry_date": date.today() + timedelta(days=5),
            "category_id": 999,
            "created_by": user.id
        })


def test_update_item(db):
    user, category = setup_user_category(db)

    item = crud.create_item(db, {
        "name": "Old",
        "quantity": 10,
        "threshold": 2,
        "price": 50.0,
        "supplier": "ABC",
        "expiry_date": date.today() + timedelta(days=5),
        "category_id": category.id,
        "created_by": user.id
    })

    updated = crud.update_item(db, item.id, {"name": "New"})
    assert updated.name == "New"


def test_delete_item(db):
    user, category = setup_user_category(db)

    item = crud.create_item(db, {
        "name": "Temp",
        "quantity": 10,
        "threshold": 2,
        "price": 50.0,
        "supplier": "ABC",
        "expiry_date": date.today() + timedelta(days=5),
        "category_id": category.id,
        "created_by": user.id
    })

    res = crud.delete_item(db, item.id)
    assert res["message"] == "Item deleted"



def test_low_stock(db):
    user, category = setup_user_category(db)

    crud.create_item(db, {
        "name": "Low",
        "quantity": 1,
        "threshold": 5,
        "price": 10,
        "supplier": "ABC",
        "expiry_date": date.today() + timedelta(days=5),
        "category_id": category.id,
        "created_by": user.id
    })

    items = crud.get_low_stock(db)
    assert len(items) == 1


def test_expiring_items(db):
    user, category = setup_user_category(db)

    crud.create_item(db, {
        "name": "Soon",
        "quantity": 10,
        "threshold": 2,
        "price": 50,
        "supplier": "ABC",
        "expiry_date": date.today() + timedelta(days=3),
        "category_id": category.id,
        "created_by": user.id
    })

    items = crud.get_expiring_items(db)
    assert len(items) == 1