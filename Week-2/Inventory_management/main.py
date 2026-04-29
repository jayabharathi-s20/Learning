from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import crud
from .schemas import *


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users")
def create_user_api(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.

    Args:
        user (UserCreate): User input data

    Returns:
        User: Created user object
    """
    try:
        return crud.create_user(db, user.model_dump())
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))
    



@app.get("/users")
def get_users_api(db: Session = Depends(get_db)):
    """
    Retrieve all users.

    Returns:
        List[User]: List of users
    """
    try:
        return crud.get_users(db)
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/users/{user_id}")
def get_user_api(user_id: int, db: Session = Depends(get_db)):
    """
    Get a user by ID.

    Args:
        user_id (int): User ID

    Returns:
        User: User object
    """
    try:
        user = crud.get_user(db, user_id)
        if not user:
            raise HTTPException(404, "User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))


@app.put("/users/{user_id}")
def update_user_api(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """
    Fully update a user.

    Args:
        user_id (int): User ID
        user (UserUpdate): Updated data

    Returns:
        User: Updated user
    """
    try:
        updated = crud.update_user(db, user_id, user.model_dump())
        if not updated:
            raise HTTPException(404, "User not found")
        return updated
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


@app.patch("/users/{user_id}")
def patch_user_api(user_id: int, user: UserPatch, db: Session = Depends(get_db)):
    """
    Partially update a user.

    Args:
        user_id (int): User ID
        user (UserPatch): Partial update data

    Returns:
        User: Updated user
    """
    try:
        updated = crud.patch_user(db, user_id, user.dict(exclude_unset=True))
        if not updated:
            raise HTTPException(404, "User not found")
        return updated
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


@app.delete("/users/{user_id}")
def delete_user_api(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user by ID.

    Args:
        user_id (int): User ID

    Returns:
        dict: Deletion message
    """
    try:
        user = crud.delete_user(db, user_id)
        if not user:
            raise HTTPException(404, "User not found")
        return user
    except Exception as e:
        raise HTTPException(500, str(e))


@app.post("/categories")
def create_category_api(category: CategoryCreate, db: Session = Depends(get_db)):
    """
    Create a new category.

    Returns:
        Category: Created category
    """
    try:
        return crud.create_category(db, category.model_dump())
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/categories")
def get_categories_api(db: Session = Depends(get_db)):
    """
    Retrieve all categories.

    Returns:
        List[Category]
    """
    try:
        return crud.get_categories(db)
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/categories/{category_id}")
def get_category_api(category_id: int, db: Session = Depends(get_db)):
    """
    Get category by ID.
    """
    try:
        category = crud.get_category(db, category_id)
        if not category:
            raise HTTPException(404, "Category not found")
        return category
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))


@app.put("/categories/{category_id}")
def update_category_api(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    """
    Fully update a category.
    """
    try:
        updated = crud.update_category(db, category_id, category.model_dump())
        if not updated:
            raise HTTPException(404, "Category not found")
        return updated
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


@app.patch("/categories/{category_id}")
def patch_category_api(category_id: int, category: CategoryPatch, db: Session = Depends(get_db)):
    """
    Partially update a category.
    """
    try:
        updated = crud.patch_category(db, category_id, category.dict(exclude_unset=True))
        if not updated:
            raise HTTPException(404, "Category not found")
        return updated
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


@app.delete("/categories/{category_id}")
def delete_category_api(category_id: int, db: Session = Depends(get_db)):
    """
    Delete a category.
    """
    try:
        category = crud.delete_category(db, category_id)
        if not category:
            raise HTTPException(404, "Category not found")
        return category
    except Exception as e:
        raise HTTPException(500, str(e))


@app.post("/items")
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """
    Create a new inventory item.
    """
    try:
        return crud.create_item(db, item.model_dump())
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/items")
def get_items(db: Session = Depends(get_db)):
    """
    Retrieve all items.
    """
    try:
        return crud.get_items(db)
    except Exception as e:
        raise HTTPException(500, str(e))
    
@app.get("/items/low-stock")
def low_stock(db: Session = Depends(get_db)):
    """
    Get items with low stock.
    """
    try:
        return crud.get_low_stock(db)
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/items/expiring-soon")
def expiring_items(db: Session = Depends(get_db)):
    """
    Get items expiring within 7 days.
    """
    try:
        return crud.get_expiring_items(db)
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/items/by-supplier")
def items_by_supplier(supplier: str, db: Session = Depends(get_db)):
    """
    Get items filtered by supplier.
    """
    try:
        return crud.get_items_by_supplier(db, supplier)
    except Exception as e:
        raise HTTPException(500, str(e))




@app.get("/items/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    """
    Get item by ID.
    """
    try:
        item = crud.get_item(db, item_id)
        if not item:
            raise HTTPException(404, "Item not found")
        return item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))


@app.put("/items/{item_id}")
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    """
    Fully update an item.
    """
    try:
        updated = crud.update_item(db, item_id, item.model_dump())
        if not updated:
            raise HTTPException(404, "Item not found")
        return updated
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


@app.patch("/items/{item_id}")
def patch_item(item_id: int, item: ItemPatch, db: Session = Depends(get_db)):
    """
    Partially update an item.
    """
    try:
        updated = crud.patch_item(db, item_id, item.dict(exclude_unset=True))
        if not updated:
            raise HTTPException(404, "Item not found")
        return updated
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """
    Delete an item.
    """
    try:
        item = crud.delete_item(db, item_id)
        if not item:
            raise HTTPException(404, "Item not found")
        return item
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/users/{user_id}/items")
def user_items(user_id: int, db: Session = Depends(get_db)):
    """
    Get items created by a user.
    """
    try:
        return crud.get_user_items(db, user_id)
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/categories/{category_id}/items")
def items_by_category(category_id: int, db: Session = Depends(get_db)):
    """
    Get items under a category.
    """
    try:
        return crud.get_items_by_category(db, category_id)
    except Exception as e:
        raise HTTPException(500, str(e))