from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from app import crud
from app.models import UserCreate, LoginSchema, UserUpdate, UserPatch, CategoryCreate, CategoryUpdate, CategoryPatch, ItemCreate, ItemUpdate, ItemPatch
from app.dependencies import  admin_only,all_roles,admin_manager,get_db
from .utils.auth import create_access_token, decode_token
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_user(db, user)
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.post("/login")
def login(data: LoginSchema, response: Response, db: Session = Depends(get_db)):
    result = crud.login_user(db, data.email, data.password)

    if not result:
        raise HTTPException(401, "Invalid credentials")

    response.set_cookie("access_token", result["access_token"], httponly=True, samesite="lax")
    response.set_cookie("refresh_token", result["refresh_token"], httponly=True, samesite="lax")

    return {"message": "Login successful"}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}


@router.post("/refresh")
def refresh_token(request: Request, response: Response):
    token = request.cookies.get("refresh_token")

    if not token:
        raise HTTPException(401, "Missing refresh token")

    payload = decode_token(token)

    if not payload or payload.get("type") != "refresh":
        raise HTTPException(401, "Invalid refresh token")

    user_id = payload.get("sub")

    new_access_token = create_access_token({"sub": user_id})

    response.set_cookie("access_token", new_access_token, httponly=True, samesite="lax")

    return {"message": "Access token refreshed"}


@router.get("/users")
def get_users(
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)):
    return crud.get_users(db)


@router.get("/users/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)):

    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user


@router.put("/users/{user_id}")
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)):

    return crud.update_user(db, user_id, user.model_dump())


@router.patch("/users/{user_id}")
def patch_user(
    user_id: int,
    user: UserPatch,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)):

    return crud.patch_user(db, user_id, user.model_dump(exclude_unset=True))


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)):

    return crud.delete_user(db, user_id)



@router.post("/categories")
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(all_roles)):
    return crud.create_category(db, category.model_dump())


@router.get("/categories")
def get_categories(
    db: Session = Depends(get_db),
    current_user=Depends(all_roles)):

    return crud.get_categories(db)


@router.get("/categories/{category_id}")
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(all_roles)):

    return crud.get_category(db, category_id)


@router.put("/categories/{category_id}")
def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_manager)):
    return crud.update_category(db, category_id, category.model_dump())


@router.patch("/categories/{category_id}")
def patch_category(
    category_id: int,
    category: CategoryPatch,
    db: Session = Depends(get_db),
    current_user=Depends(admin_manager)):

    return crud.patch_category(db, category_id, category.model_dump(exclude_unset=True))


@router.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)):
    return crud.delete_category(db, category_id)


@router.post("/items")
def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user=Depends(all_roles)):

    data = item.model_dump()
    data["created_by"] = current_user.id
    return crud.create_item(db, data)


@router.get("/items")
def get_items(
    db: Session = Depends(get_db),
    current_user=Depends(all_roles)):

    return crud.get_items(db)




@router.get("/items/low-stock")
def low_stock(
    db: Session = Depends(get_db),
    current_user=Depends(all_roles)):

    return crud.get_low_stock(db)




@router.get("/items/by-supplier")
def items_by_supplier(
    supplier: str,
    db: Session = Depends(get_db),
    current_user=Depends(all_roles)):

    return crud.get_items_by_supplier(db, supplier)

@router.get("/users/{user_id}/items")
def user_items(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(all_roles)):

    return crud.get_user_items(db, user_id)


@router.get("/categories/{category_id}/items")
def items_by_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(all_roles)):

    return crud.get_items_by_category(db, category_id)



@router.get("/items/expiring-soon")
def expiring_items(
    db: Session = Depends(get_db),
    current_user=Depends(all_roles)):

    return crud.get_expiring_items(db)

@router.get("/items/{item_id}")
def get_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(all_roles)):

    return crud.get_item(db, item_id)



@router.put("/items/{item_id}")
def update_item(
    item_id: int,
    item: ItemUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_manager)):

    return crud.update_item(db, item_id, item.model_dump())


@router.patch("/items/{item_id}")
def patch_item(
    item_id: int,
    item: ItemPatch,
    db: Session = Depends(get_db),
    current_user=Depends(admin_manager)):

    return crud.patch_item(db, item_id, item.model_dump(exclude_unset=True))


@router.delete("/items/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)):

    return crud.delete_item(db, item_id)















