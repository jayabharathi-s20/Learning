from datetime import date, timedelta


# ---------------- USERS ----------------

def test_create_user_api(client):
    res = client.post("/users", json={
        "name": "John",
        "email": "john@test.com"
    })
    assert res.status_code == 200
    assert res.json()["email"] == "john@test.com"



def test_get_users_api(client):
    res = client.get("/users")
    assert res.status_code == 200


def test_get_user_by_id_api(client):
    user = client.post("/users", json={
        "name": "Test",
        "email": "get@test.com"
    }).json()

    res = client.get(f"/users/{user['id']}")
    assert res.status_code == 200


def test_get_user_not_found_api(client):
    res = client.get("/users/999")
    assert res.status_code == 404


def test_update_user_api(client):
    user = client.post("/users", json={
        "name": "Old",
        "email": "old@test.com"
    }).json()

    res = client.put(f"/users/{user['id']}", json={
        "name": "New",
        "email": "new@test.com"
    })

    assert res.status_code == 200
    assert res.json()["name"] == "New"


def test_patch_user_api(client):
    user = client.post("/users", json={
        "name": "Patch",
        "email": "patch@test.com"
    }).json()

    res = client.patch(f"/users/{user['id']}", json={"name": "Updated"})
    assert res.status_code == 200
    assert res.json()["name"] == "Updated"


def test_delete_user_api(client):
    user = client.post("/users", json={
        "name": "Delete",
        "email": "delete@test.com"
    }).json()

    res = client.delete(f"/users/{user['id']}")
    assert res.status_code == 200


# ---------------- CATEGORIES ----------------

def test_create_category_api(client):
    res = client.post("/categories", json={"name": "Medicine"})
    assert res.status_code == 200


def test_duplicate_category_api(client):
    client.post("/categories", json={"name": "Food"})

    res = client.post("/categories", json={"name": "Food"})
    assert res.status_code == 400


def test_get_categories_api(client):
    res = client.get("/categories")
    assert res.status_code == 200


def test_get_category_by_id_api(client):
    category = client.post("/categories", json={"name": "TestCat"}).json()

    res = client.get(f"/categories/{category['id']}")
    assert res.status_code == 200


def test_delete_category_api(client):
    category = client.post("/categories", json={"name": "DeleteCat"}).json()

    res = client.delete(f"/categories/{category['id']}")
    assert res.status_code == 200


# ---------------- ITEMS ----------------

def create_user_and_category(client):
    user = client.post("/users", json={
        "name": "ItemUser",
        "email": "itemuser@test.com"
    }).json()

    category = client.post("/categories", json={
        "name": "ItemCat"
    }).json()

    return user, category


def test_create_item_api(client):
    user, category = create_user_and_category(client)

    res = client.post("/items", json={
        "name": "Rice",
        "quantity": 10,
        "threshold": 2,
        "price": 50,
        "supplier": "ABC",
        "expiry_date": str(date.today() + timedelta(days=5)),
        "category_id": category["id"],
        "created_by": user["id"]
    })

    assert res.status_code == 200


def test_get_items_api(client):
    res = client.get("/items")
    assert res.status_code == 200


def test_get_item_by_id_api(client):
    user, category = create_user_and_category(client)

    item = client.post("/items", json={
        "name": "Milk",
        "quantity": 5,
        "threshold": 2,
        "price": 30,
        "supplier": "ABC",
        "expiry_date": str(date.today() + timedelta(days=5)),
        "category_id": category["id"],
        "created_by": user["id"]
    }).json()

    res = client.get(f"/items/{item['id']}")
    assert res.status_code == 200


def test_update_item_api(client):
    user, category = create_user_and_category(client)

    item = client.post("/items", json={
        "name": "Old",
        "quantity": 5,
        "threshold": 2,
        "price": 30,
        "supplier": "ABC",
        "expiry_date": str(date.today() + timedelta(days=5)),
        "category_id": category["id"],
        "created_by": user["id"]
    }).json()

    res = client.put(f"/items/{item['id']}", json={
        "name": "New",
        "quantity": 10,
        "threshold": 3,
        "price": 60,
        "supplier": "XYZ",
        "expiry_date": str(date.today() + timedelta(days=10)),
        "category_id": category["id"],
        "created_by": user["id"]
    })

    assert res.status_code == 200


def test_delete_item_api(client):
    user, category = create_user_and_category(client)

    item = client.post("/items", json={
        "name": "Delete",
        "quantity": 5,
        "threshold": 2,
        "price": 30,
        "supplier": "ABC",
        "expiry_date": str(date.today() + timedelta(days=5)),
        "category_id": category["id"],
        "created_by": user["id"]
    }).json()

    res = client.delete(f"/items/{item['id']}")
    assert res.status_code == 200


# ---------------- FILTER APIs ----------------

def test_low_stock_api(client):
    res = client.get("/items/low-stock")
    assert res.status_code == 200


def test_expiring_items_api(client):
    res = client.get("/items/expiring-soon")
    assert res.status_code == 200


def test_items_by_supplier_api(client):
    res = client.get("/items/by-supplier?supplier=ABC")
    assert res.status_code == 200


def test_user_items_api(client):
    user = client.post("/users", json={
        "name": "UserItems",
        "email": "ui@test.com"
    }).json()

    res = client.get(f"/users/{user['id']}/items")
    assert res.status_code == 200


def test_items_by_category_api(client):
    category = client.post("/categories", json={"name": "CatItems"}).json()

    res = client.get(f"/categories/{category['id']}/items")
    assert res.status_code == 200