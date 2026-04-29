import pytest
from datetime import date, timedelta
from Inventory_management import crud



@pytest.fixture
def user_data():
    """
    Provides valid user data.

    Returns:
        dict: User payload
    """
    return {"name": "John", "email": "john@test.com"}


@pytest.fixture
def category_data():
    """
    Provides valid category data.

    Returns:
        dict: Category payload
    """
    return {"name": "Medicine"}


@pytest.fixture
def item_base_data():
    """
    Provides base item data (without foreign keys).

    Returns:
        dict: Item payload
    """
    return {
        "name": "Paracetamol",
        "quantity": 10,
        "threshold": 2,
        "price": 50.0,
        "supplier": "ABC",
        "expiry_date": date.today() + timedelta(days=5),
    }


@pytest.fixture
def user(db, user_data):
    """
    Creates a user in test DB.

    Args:
        db: Database session
        user_data: Input data

    Returns:
        User: Created user object
    """
    return crud.create_user(db, user_data)


@pytest.fixture
def category(db, category_data):
    """
    Creates a category in test DB.

    Returns:
        Category: Created category
    """
    return crud.create_category(db, category_data)


@pytest.fixture
def item(db, user, category, item_base_data):
    """
    Creates an item with valid foreign keys.

    Returns:
        Item: Created item
    """
    data = item_base_data.copy()
    data.update({
        "category_id": category.id,
        "created_by": user.id
    })
    return crud.create_item(db, data)


def test_create_user(db, user_data):
    """
    Test creating a user.

    Asserts:
        User ID is generated
        Email matches input
    """
    user = crud.create_user(db, user_data)

    assert user.id is not None
    assert user.email == user_data["email"]


def test_create_user_duplicate(db):
    """
    Test duplicate email raises ValueError.

    Raises:
        ValueError
    """
    crud.create_user(db, {"name": "A", "email": "dup@test.com"})

    with pytest.raises(ValueError):
        crud.create_user(db, {"name": "B", "email": "dup@test.com"})


def test_get_user(db, user):
    """
    Test retrieving existing user.

    Asserts:
        Returned user matches created user
    """
    fetched = crud.get_user(db, user.id)

    assert fetched.id == user.id


def test_get_user_not_found(db):
    """
    Test retrieving non-existing user.

    Asserts:
        Returns None
    """
    assert crud.get_user(db, 999) is None


def test_get_users(db, user):
    """
    Test retrieving all users.

    Asserts:
        At least one user exists
    """
    users = crud.get_users(db)

    assert len(users) >= 1


def test_update_user(db, user):
    """
    Test full update of user.

    Asserts:
        Name is updated
    """
    updated = crud.update_user(db, user.id, {"name": "Updated"})

    assert updated.name == "Updated"


def test_update_user_not_found(db):
    """
    Test updating non-existing user.

    """
    assert crud.update_user(db, 999, {"name": "X"}) is None


def test_patch_user(db, user):
    """
    Test partial update of user.

    Asserts:
        Only provided field is updated
    """
    updated = crud.patch_user(db, user.id, {"name": "Patch"})

    assert updated.name == "Patch"


def test_delete_user(db, user):
    """
    Test deleting user.

    Asserts:
        Success message returned
    """
    res = crud.delete_user(db, user.id)

    assert res["message"] == "User deleted"


def test_delete_user_not_found(db):
    """
    Test deleting non-existing user.

    Asserts:
        Returns None
    """
    assert crud.delete_user(db, 999) is None



def test_create_category(db, category_data):
    """Test category creation."""
    category = crud.create_category(db, category_data)

    assert category.id is not None


def test_duplicate_category(db, category_data):
    """
    Test duplicate category.

    Raises:
        ValueError
    """
    crud.create_category(db,category_data)

    with pytest.raises(ValueError):
        crud.create_category(db, category_data)


def test_get_category(db, category):
    """Test retrieving category by ID."""
    fetched = crud.get_category(db, category.id)

    assert fetched.id == category.id


def test_get_categories(db, category):
    """Test retrieving all categories."""
    categories = crud.get_categories(db)

    assert len(categories) >= 1


def test_update_category(db, category):
    """Test updating category."""
    updated = crud.update_category(db, category.id, {"name": "New"})

    assert updated.name == "New"


def test_patch_category(db, category):
    """Test partial update."""
    updated = crud.patch_category(db, category.id, {"name": "Patch"})

    assert updated.name == "Patch"


def test_delete_category(db, category):
    """Test deleting category."""
    res = crud.delete_category(db, category.id)

    assert res["message"] == "Category deleted"


def test_delete_category_not_found(db):
    """Test deleting non-existing category."""
    assert crud.delete_category(db, 999) is None



def test_create_item(db, user, category, item_base_data):
    """
    Test item creation.

    Asserts:
        Item is created with ID
    """
    data = item_base_data.copy()
    data.update({
        "category_id": category.id,
        "created_by": user.id
    })

    item = crud.create_item(db, data)

    assert item.id is not None


def test_create_item_invalid_category(db, user, item_base_data):
    """
    Test invalid category.

    Raises:
        ValueError
    """
    data = item_base_data.copy()
    data.update({
        "category_id": 999,
        "created_by": user.id
    })

    with pytest.raises(ValueError):
        crud.create_item(db, data)


def test_create_item_invalid_user(db, category, item_base_data):
    """
    Test invalid user.

    Raises:
        ValueError
    """
    data = item_base_data.copy()
    data.update({
        "category_id": category.id,
        "created_by": 999
    })

    with pytest.raises(ValueError):
        crud.create_item(db, data)


def test_get_item(db, item):
    """Test retrieving item by ID."""
    fetched = crud.get_item(db, item.id)

    assert fetched.id == item.id


def test_get_items(db, item):
    """Test retrieving all items."""
    items = crud.get_items(db)

    assert len(items) >= 1


def test_update_item(db, item):
    """Test full update of item."""
    updated = crud.update_item(db, item.id, {"name": "Updated"})

    assert updated.name == "Updated"


def test_update_item_invalid_category(db, item):
    """
    Test invalid category update.

    Raises:
        ValueError
    """
    with pytest.raises(ValueError):
        crud.update_item(db, item.id, {"category_id": 999})


def test_patch_item(db, item):
    """Test partial update."""
    updated = crud.patch_item(db, item.id, {"name": "Patch"})

    assert updated.name == "Patch"


def test_delete_item(db, item):
    """Test deleting item."""
    res = crud.delete_item(db, item.id)

    assert res["message"] == "Item deleted"


def test_delete_item_not_found(db):
    """Test deleting non-existing item."""
    assert crud.delete_item(db, 999) is None


# =========================
# FILTER TESTS
# =========================

def test_low_stock(db, user, category, item_base_data):
    """Test low stock filter."""
    data = item_base_data.copy()
    data.update({
        "quantity": 1,
        "threshold": 5,
        "category_id": category.id,
        "created_by": user.id
    })

    crud.create_item(db, data)

    items = crud.get_low_stock(db)

    assert len(items) == 1


def test_expiring_items(db, user, category, item_base_data):
    """Test expiring items filter."""
    data = item_base_data.copy()
    data.update({
        "expiry_date": date.today() + timedelta(days=3),
        "category_id": category.id,
        "created_by": user.id
    })

    crud.create_item(db, data)

    items = crud.get_expiring_items(db)

    assert len(items) == 1


def test_get_items_by_supplier(db, item):
    """Test supplier filter."""
    items = crud.get_items_by_supplier(db, "ABC")

    assert len(items) >= 1


def test_get_user_items(db, user, item):
    """Test user-specific items."""
    items = crud.get_user_items(db, user.id)

    assert len(items) >= 1


def test_get_items_by_category(db, category, item):
    """Test category filter."""
    items = crud.get_items_by_category(db, category.id)

    assert len(items) >= 1