import pytest
from datetime import date, timedelta
from Inventory_management import crud




@pytest.fixture
def user_data():
    """Valid user payload."""
    return {"name": "John", "email": "john@test.com"}


@pytest.fixture
def category_data():
    """Valid category payload."""
    return {"name": "Medicine"}


@pytest.fixture
def item_data():
    """Base item payload (without FK)."""
    return {
        "name": "Paracetamol",
        "quantity": 10,
        "threshold": 2,
        "price": 50,
        "supplier": "ABC",
        "expiry_date": date.today() + timedelta(days=5),
    }


@pytest.fixture
def user(db, user_data):
    """Create a user."""
    return crud.create_user(db, user_data)


@pytest.fixture
def category(db, category_data):
    """Create a category."""
    return crud.create_category(db, category_data)


@pytest.fixture
def item(db, user, category, item_data):
    """Create an item with valid FK."""
    data = item_data.copy()
    data.update({
        "category_id": category.id,
        "created_by": user.id
    })
    return crud.create_item(db, data)




def test_create_user(db, user_data):
    """Test user creation."""
    try:
        user = crud.create_user(db, user_data)
        assert user.id is not None
        assert user.email == user_data["email"]
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")


def test_create_user_duplicate(db):
    """Test duplicate email raises ValueError."""
    crud.create_user(db, {"name": "A", "email": "dup@test.com"})

    with pytest.raises(ValueError):
        crud.create_user(db, {"name": "B", "email": "dup@test.com"})


def test_get_user(db, user):
    """Test fetching user."""
    fetched = crud.get_user(db, user.id)
    assert fetched.id == user.id


def test_get_user_not_found(db):
    """Test user not found."""
    assert crud.get_user(db, 999) is None


def test_update_user(db, user):
    """Test updating user."""
    updated = crud.update_user(db, user.id, {"name": "Updated"})
    assert updated.name == "Updated"


def test_update_user_duplicate_email(db, user):
    """Test updating with duplicate email."""
    crud.create_user(db, {"name": "Other", "email": "other@test.com"})

    with pytest.raises(ValueError):
        crud.update_user(db, user.id, {"email": "other@test.com"})


def test_patch_user(db, user):
    """Test partial update."""
    updated = crud.patch_user(db, user.id, {"name": "Patch"})
    assert updated.name == "Patch"


def test_delete_user(db, user):
    """Test deleting user."""
    res = crud.delete_user(db, user.id)
    assert res["message"] == "User deleted"


def test_delete_user_not_found(db):
    """Test deleting non-existing user."""
    assert crud.delete_user(db, 999) is None




def test_create_category(db, category_data):
    """Test category creation."""
    category = crud.create_category(db, category_data)
    assert category.id is not None


def test_duplicate_category(db, category_data):
    """Test duplicate category."""
    crud.create_category(db, category_data)

    with pytest.raises(ValueError):
        crud.create_category(db, category_data)


def test_get_category(db, category):
    """Test fetching category."""
    fetched = crud.get_category(db, category.id)
    assert fetched.id == category.id


def test_update_category_duplicate(db, category):
    """Test duplicate category update."""
    crud.create_category(db, {"name": "Other"})

    with pytest.raises(ValueError):
        crud.update_category(db, category.id, {"name": "Other"})


def test_patch_category(db, category):
    """Test partial update."""
    updated = crud.patch_category(db, category.id, {"name": "Patch"})
    assert updated.name == "Patch"


def test_delete_category(db, category):
    """Test delete category."""
    res = crud.delete_category(db, category.id)
    assert res["message"] == "Category deleted"


# =========================
# ITEM TESTS
# =========================

def test_create_item(db, user, category, item_data):
    """Test item creation."""
    data = item_data.copy()
    data.update({
        "category_id": category.id,
        "created_by": user.id
    })

    item = crud.create_item(db, data)
    assert item.id is not None


def test_create_item_invalid_category(db, user, item_data):
    """Test invalid category."""
    data = item_data.copy()
    data.update({
        "category_id": 999,
        "created_by": user.id
    })

    with pytest.raises(ValueError):
        crud.create_item(db, data)


def test_create_item_invalid_user(db, category, item_data):
    """Test invalid user."""
    data = item_data.copy()
    data.update({
        "category_id": category.id,
        "created_by": 999
    })

    with pytest.raises(ValueError):
        crud.create_item(db, data)


def test_update_item_invalid_category(db, item):
    """Test invalid category update."""
    with pytest.raises(ValueError):
        crud.update_item(db, item.id, {"category_id": 999})


def test_update_item_invalid_user(db, item):
    """Test invalid user update."""
    with pytest.raises(ValueError):
        crud.update_item(db, item.id, {"created_by": 999})


def test_patch_item(db, item):
    """Test patch item."""
    updated = crud.patch_item(db, item.id, {"name": "Patch"})
    assert updated.name == "Patch"


def test_delete_item(db, item):
    """Test delete item."""
    res = crud.delete_item(db, item.id)
    assert res["message"] == "Item deleted"


def test_delete_item_not_found(db):
    """Test deleting non-existing item."""
    assert crud.delete_item(db, 999) is None




def test_low_stock(db, user, category, item_data):
    """Test low stock filter."""
    data = item_data.copy()
    data.update({
        "quantity": 1,
        "threshold": 5,
        "category_id": category.id,
        "created_by": user.id
    })

    crud.create_item(db, data)

    items = crud.get_low_stock(db)
    assert len(items) == 1


def test_expiring_items(db, user, category, item_data):
    """Test expiring items."""
    data = item_data.copy()
    data.update({
        "expiry_date": date.today() + timedelta(days=3),
        "category_id": category.id,
        "created_by": user.id
    })

    crud.create_item(db, data)

    items = crud.get_expiring_items(db)
    assert len(items) == 1


def test_items_by_supplier(db, item):
    """Test supplier filter."""
    items = crud.get_items_by_supplier(db, "ABC")
    assert len(items) >= 1


def test_user_items(db, user, item):
    """Test user items."""
    items = crud.get_user_items(db, user.id)
    assert len(items) >= 1


def test_items_by_category(db, category, item):
    """Test category filter."""
    items = crud.get_items_by_category(db, category.id)
    assert len(items) >= 1