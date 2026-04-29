
from datetime import date, timedelta



def test_create_user_api(client):
    res = client.post("/users", json={
        "name": "John",
        "email": "john@test.com"
    })

    assert res.status_code == 200
    assert res.json()["email"] == "john@test.com"


def test_duplicate_user_api(client):
    client.post("/users", json={
        "name": "John",
        "email": "dup@test.com"
    })

    res = client.post("/users", json={
        "name": "Jane",
        "email": "dup@test.com"
    })

    assert res.status_code == 400


def test_get_users_api(client):
    client.post("/users", json={
        "name": "John",
        "email": "john@test.com"
    })

    res = client.get("/users")

    assert res.status_code == 200
    assert len(res.json()) == 1


def test_get_user_by_id_api(client):
    user = client.post("/users", json={
        "name": "John",
        "email": "john@test.com"
    }).json()

    res = client.get(f"/users/{user['id']}")

    assert res.status_code == 200
    assert res.json()["name"] == "John"


def test_update_user_api(client):
    user = client.post("/users", json={
        "name": "John",
        "email": "john@test.com"
    }).json()

    res = client.put(f"/users/{user['id']}", json={
        "name": "Updated",
        "email": "updated@test.com"
    })

    assert res.status_code == 200
    assert res.json()["name"] == "Updated"


def test_delete_user_api(client):
    user = client.post("/users", json={
        "name": "John",
        "email": "john@test.com"
    }).json()

    res = client.delete(f"/users/{user['id']}")

    assert res.status_code == 200
    assert res.json()["message"] == "User deleted"



def test_create_category_api(client):
    res = client.post("/categories", json={"name": "Medicine"})

    assert res.status_code == 200
    assert res.json()["name"] == "Medicine"


def test_duplicate_category_api(client):
    client.post("/categories", json={"name": "Medicine"})

    res = client.post("/categories", json={"name": "Medicine"})

    assert res.status_code == 400



def setup_user_category(client):
    user = client.post("/users", json={
        "name": "John",
        "email": "john@test.com"
    }).json()

    category = client.post("/categories", json={
        "name": "Medicine"
    }).json()

    return user, category


def test_create_item_api(client):
    user, category = setup_user_category(client)

    res = client.post("/items", json={
        "name": "Paracetamol",
        "quantity": 10,
        "threshold": 2,
        "price": 50,
        "supplier": "ABC",
        "expiry_date": str(date.today() + timedelta(days=5)),
        "category_id": category["id"],
        "created_by": user["id"]
    })

    assert res.status_code == 200
    assert res.json()["name"] == "Paracetamol"


def test_low_stock_api(client):
    user, category = setup_user_category(client)

    client.post("/items", json={
        "name": "Low",
        "quantity": 1,
        "threshold": 5,
        "price": 10,
        "supplier": "ABC",
        "expiry_date": str(date.today() + timedelta(days=5)),
        "category_id": category["id"],
        "created_by": user["id"]
    })

    res = client.get("/items/low-stock")

    assert res.status_code == 200
    assert len(res.json()) == 1


def test_expiring_items_api(client):
    user, category = setup_user_category(client)

    client.post("/items", json={
        "name": "Soon",
        "quantity": 10,
        "threshold": 2,
        "price": 50,
        "supplier": "ABC",
        "expiry_date": str(date.today() + timedelta(days=3)),
        "category_id": category["id"],
        "created_by": user["id"]
    })

    res = client.get("/items/expiring-soon")

    assert res.status_code == 200
    assert len(res.json()) == 1


def test_items_by_supplier_api(client):
    user, category = setup_user_category(client)

    client.post("/items", json={
        "name": "Item1",
        "quantity": 10,
        "threshold": 2,
        "price": 50,
        "supplier": "ABC",
        "expiry_date": str(date.today() + timedelta(days=5)),
        "category_id": category["id"],
        "created_by": user["id"]
    })

    res = client.get("/items/by-supplier?supplier=ABC")

    assert res.status_code == 200
    assert len(res.json()) == 1


def test_get_item_api(client):
    user, category = setup_user_category(client)

    item = client.post("/items", json={
        "name": "Item",
        "quantity": 10,
        "threshold": 2,
        "price": 50,
        "supplier": "ABC",
        "expiry_date": str(date.today() + timedelta(days=5)),
        "category_id": category["id"],
        "created_by": user["id"]
    }).json()

    res = client.get(f"/items/{item['id']}")

    assert res.status_code == 200
    assert res.json()["name"] == "Item"


def test_delete_item_api(client):
    user, category = setup_user_category(client)

    item = client.post("/items", json={
        "name": "Temp",
        "quantity": 10,
        "threshold": 2,
        "price": 50,
        "supplier": "ABC",
        "expiry_date": str(date.today() + timedelta(days=5)),
        "category_id": category["id"],
        "created_by": user["id"]
    }).json()

    res = client.delete(f"/items/{item['id']}")

    assert res.status_code == 200
    assert res.json()["message"] == "Item deleted"