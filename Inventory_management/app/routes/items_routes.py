from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..controllers import item_controllers
from ..models import ItemCreate, ItemUpdate, ItemPatch
from ..utils.dependencies import admin_only, all_roles, admin_manager, get_db
from ..constants import *


router = APIRouter()


@router.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user = Depends(all_roles)
):
    """
    Create a new item.
    """
    try:
        data = item.model_dump()
        data["created_by"] = current_user.id

        created_item = item_controllers.create_item(db, data)

        return created_item

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error_code": "CREATE_ITEM_FAILED",
                "message": str(e)
            }
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error_code": "CREATE_ITEM_INTERNAL_ERROR",
                "message": INTERNAL_SERVER_ERROR
            }
        )


@router.get("/items", status_code=status.HTTP_200_OK)
def get_items(
    db: Session = Depends(get_db),
    current_user=Depends(all_roles)
):
    """
    Retrieve all items.
    """
    try:
        items = item_controllers.get_items(db)

        return items

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error_code": "FETCH_ITEMS_FAILED",
                "message": INTERNAL_SERVER_ERROR
            }
        )


@router.get("/items/low-stock", status_code=status.HTTP_200_OK)
def low_stock(
    db: Session = Depends(get_db),
    current_user=Depends(all_roles)
):
    """
    Retrieve low stock items.
    """
    try:
        items = item_controllers.get_low_stock(db)

        if not items["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "error_code": "NO_LOW_STOCK_ITEMS",
                    "message": NO_LOW_STOCK_ITEMS
                }
            )

        return items

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error_code": "FETCH_LOW_STOCK_ITEMS_FAILED",
                "message": INTERNAL_SERVER_ERROR
            }
        )


@router.get("/items/by-supplier", status_code=status.HTTP_200_OK)
def items_by_supplier(
    supplier: str,
    db: Session = Depends(get_db),
    current_user=Depends(all_roles)
):
    """
    Retrieve items by supplier.
    """
    try:
        result = item_controllers.get_items_by_supplier(db, supplier)

        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "error_code": "SUPPLIER_NOT_FOUND",
                    "message": SUPPLIER_NOT_FOUND
                }
            )

        return result

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error_code": "FETCH_SUPPLIER_ITEMS_FAILED",
                "message": INTERNAL_SERVER_ERROR
            }
        )


@router.get("/users/{user_id}/items", status_code=status.HTTP_200_OK)
def user_items(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(all_roles)
):
    """
    Retrieve items created by a user.
    """
    try:
        items = item_controllers.get_user_items(db, user_id)

        if not items["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "error_code": "USER_ITEMS_NOT_FOUND",
                    "message": USER_ITEMS_NOT_FOUND
                }
            )

        return items
    
    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error_code": "FETCH_USER_ITEMS_FAILED",
                "message": INTERNAL_SERVER_ERROR
            }
        )


@router.get("/categories/{category_id}/items", status_code=status.HTTP_200_OK)
def items_by_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(all_roles)
):
    """
    Retrieve items by category.
    """
    try:
        items = item_controllers.get_items_by_category(db, category_id)

        if not items["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "error_code": "CATEGORY NOT FOUND",
                    "message": CATEGORY_NOT_FOUND
                }
            )

        return items

    except HTTPException:
        raise


    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error_code": "FETCH_CATEGORY_ITEMS_FAILED",
                "message": INTERNAL_SERVER_ERROR
            }
        )


@router.get("/items/expiring-soon", status_code=status.HTTP_200_OK)
def expiring_items(
    db: Session = Depends(get_db),
    current_user=Depends(all_roles)
):
    """
    Retrieve items that are expiring soon.
    """
    try:
        items = item_controllers.get_expiring_items(db)

        if not items["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "error_code": "NO_EXPIRING_ITEMS_FOUND",
                    "message": NO_EXPIRING_ITEMS_FOUND
                }
            )

        return items
    
    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error_code": "FETCH_EXPIRING_ITEMS_FAILED",
                "message": INTERNAL_SERVER_ERROR
            }
        )


@router.get("/items/{item_id}", status_code=status.HTTP_200_OK)
def get_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(all_roles)
):
    """
    Retrieve an item by ID.
    """
    try:
        item = item_controllers.get_item(db, item_id)

        if not item["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "error_code": "ITEM_NOT_FOUND",
                    "message": ITEM_NOT_FOUND
                }
            )

        return item

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error_code": "FETCH_ITEM_FAILED",
                "message": INTERNAL_SERVER_ERROR
            }
        )


@router.put("/items/{item_id}", status_code=status.HTTP_200_OK)
def update_item(
    item_id: int,
    item: ItemUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_manager)
):
    """
    Fully update an item.
    """
    try:
        updated_item = item_controllers.update_item(
            db,
            item_id,
            item.model_dump()
        )

        if not updated_item["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "error_code": "ITEM_NOT_FOUND",
                    "message": ITEM_NOT_FOUND
                }
            )

        return updated_item

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error_code": "UPDATE_ITEM_FAILED",
                "message": str(e)
            }
        )

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error_code": "UPDATE_ITEM_INTERNAL_ERROR",
                "message": INTERNAL_SERVER_ERROR
            }
        )


@router.patch("/items/{item_id}", status_code=status.HTTP_200_OK)
def patch_item(
    item_id: int,
    item: ItemPatch,
    db: Session = Depends(get_db),
    current_user=Depends(admin_manager)
):
    """
    Partially update an item.
    """
    try:
        patched_item = item_controllers.patch_item(
            db,
            item_id,
            item.model_dump(exclude_unset=True)
        )

        if not patched_item["success"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "error_code": "ITEM_NOT_FOUND",
                    "message": ITEM_NOT_FOUND
                }
            )

        return patched_item

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error_code": "PATCH_ITEM_FAILED",
                "message": str(e)
            }
        )

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error_code": "PATCH_ITEM_INTERNAL_ERROR",
                "message": INTERNAL_SERVER_ERROR
            }
        )


@router.delete("/items/{item_id}", status_code=status.HTTP_200_OK)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    """
    Delete an item.
    """
    try:
        deleted_item = item_controllers.delete_item(db, item_id)

        if not deleted_item["success"]:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success":False,
                "error_code":"ITEM NOT FOUND",
                "message":ITEM_NOT_FOUND
            }
            )

        return deleted_item

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error_code": "DELETE_ITEM_FAILED",
                "message": INTERNAL_SERVER_ERROR
            }
        )