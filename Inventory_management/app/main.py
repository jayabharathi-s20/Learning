from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud
from app.models import *
from app.dependencies import get_current_user

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_user(db, user)
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.post("/login")
def login(
    data: LoginSchema,
    response: Response,
    db: Session = Depends(get_db)
):
    result = crud.login_user(db, data.email, data.password)

    if not result:
        raise HTTPException(401, "Invalid credentials")

    response.set_cookie(
        key="access_token",
        value=result["access_token"],
        httponly=True,
        samesite="lax"
    )

    return {"message": "Login successful"}


@app.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}



@app.get("/users")
def get_users(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.get_users(db)


@app.get("/users/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    user = crud.get_user(db, user_id)

    if not user:
        raise HTTPException(404, "User not found")

    return user


@app.put("/users/{user_id}")
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        updated = crud.update_user(db, user_id, user.model_dump())

        if not updated:
            raise HTTPException(404, "User not found")

        return updated

    except ValueError as e:
        raise HTTPException(400, str(e))


@app.patch("/users/{user_id}")
def patch_user(
    user_id: int,
    user: UserPatch,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        updated = crud.patch_user(
            db, user_id, user.model_dump(exclude_unset=True)
        )

        if not updated:
            raise HTTPException(404, "User not found")

        return updated

    except ValueError as e:
        raise HTTPException(400, str(e))


@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    deleted = crud.delete_user(db, user_id)

    if not deleted:
        raise HTTPException(404, "User not found")

    return deleted



@app.post("/categories")
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        return crud.create_category(db, category.model_dump())
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.get("/categories")
def get_categories(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.get_categories(db)


@app.get("/categories/{category_id}")
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    category = crud.get_category(db, category_id)

    if not category:
        raise HTTPException(404, "Category not found")

    return category


@app.put("/categories/{category_id}")
def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        updated = crud.update_category(db, category_id, category.model_dump())

        if not updated:
            raise HTTPException(404, "Category not found")

        return updated

    except ValueError as e:
        raise HTTPException(400, str(e))


@app.patch("/categories/{category_id}")
def patch_category(
    category_id: int,
    category: CategoryPatch,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        updated = crud.patch_category(
            db, category_id, category.model_dump(exclude_unset=True)
        )

        if not updated:
            raise HTTPException(404, "Category not found")

        return updated

    except ValueError as e:
        raise HTTPException(400, str(e))


@app.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    deleted = crud.delete_category(db, category_id)

    if not deleted:
        raise HTTPException(404, "Category not found")

    return deleted



@app.post("/items")
def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        data = item.model_dump()
        data["created_by"] = current_user.id  
        return crud.create_item(db, data)
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.get("/items")
def get_items(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.get_items(db)

@app.get("/items/low-stock")
def low_stock(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.get_low_stock(db)


@app.get("/items/expiring-soon")
def expiring_items(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.get_expiring_items(db)


@app.get("/items/by-supplier")
def items_by_supplier(
    supplier: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.get_items_by_supplier(db, supplier)


@app.get("/users/{user_id}/items")
def user_items(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.get_user_items(db, user_id)


@app.get("/categories/{category_id}/items")
def items_by_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.get_items_by_category(db, category_id)


@app.get("/items/{item_id}")
def get_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    item = crud.get_item(db, item_id)

    if not item:
        raise HTTPException(404, "Item not found")

    return item


@app.put("/items/{item_id}")
def update_item(
    item_id: int,
    item: ItemUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        updated = crud.update_item(db, item_id, item.model_dump())

        if not updated:
            raise HTTPException(404, "Item not found")

        return updated

    except ValueError as e:
        raise HTTPException(400, str(e))


@app.patch("/items/{item_id}")
def patch_item(
    item_id: int,
    item: ItemPatch,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        updated = crud.patch_item(
            db, item_id, item.model_dump(exclude_unset=True)
        )

        if not updated:
            raise HTTPException(404, "Item not found")

        return updated

    except ValueError as e:
        raise HTTPException(400, str(e))


@app.delete("/items/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    deleted = crud.delete_item(db, item_id)

    if not deleted:
        raise HTTPException(404, "Item not found")

    return deleted






