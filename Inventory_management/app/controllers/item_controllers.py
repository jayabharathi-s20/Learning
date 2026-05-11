from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from datetime import date, timedelta

from ..models import Item, Category, User
from ..constants import *


def create_item(db: Session, data: dict):
    """
    Create a new inventory item.

    This function:
    - Validates category existence
    - Validates creator existence
    - Stores the item in the database

    Args:
        db (Session):
            Active SQLAlchemy database session.

        data (dict):
            Item payload containing item details.

    Returns:
        dict:
            Returns success or failure response with item data.
    """

    try:
        if not db.query(Category).filter(
            Category.id == data["category_id"]
        ).first():
            return {
                "success": False,
                "message": INVALID_CATEGORY_ID
            }

        if not db.query(User).filter(
            User.id == data["created_by"]
        ).first():
            return {
                "success": False,
                "message": INVALID_CREATED_BY
            }

        item = Item(**data)

        db.add(item)
        db.commit()
        db.refresh(item)

        return {
            "success": True,
            "message": ITEM_CREATED_SUCCESS,
            "data": item
        }

    except IntegrityError:
        db.rollback()

        return {
            "success": False,
            "message": ITEM_CREATION_ERROR
        }

    except SQLAlchemyError as e:
        db.rollback()

        return {
            "success": False,
            "message": DATABASE_ERROR,
            "error": str(e)
        }

    except Exception as e:
        db.rollback()

        return {
            "success": False,
            "message": CREATE_ITEM_FAILED,
            "error": str(e)
        }


def get_items(db: Session):
    """
    Retrieve all inventory items.

    Args:
        db (Session):
            Active SQLAlchemy database session.

    Returns:
        dict:
            Returns list of items or failure response.
    """

    try:
        items = db.query(Item).all()

        return {
            "success": True,
            "message": ITEMS_FETCHED_SUCCESS,
            "data": items
        }

    except Exception as e:
        return {
            "success": False,
            "message": FETCH_ITEMS_FAILED,
            "error": str(e)
        }


def get_item(db: Session, item_id: int):
    """
    Retrieve an item by ID.

    Args:
        db (Session):
            Active SQLAlchemy database session.

        item_id (int):
            Item ID.

    Returns:
        dict:
            Returns item data or failure response.
    """

    try:
        item = db.query(Item).filter(
            Item.id == item_id
        ).first()

        if not item:
            return {
                "success": False,
                "message": ITEM_NOT_FOUND
            }

        return {
            "success": True,
            "message": ITEM_FETCHED_SUCCESS,
            "data": item
        }

    except Exception as e:
        return {
            "success": False,
            "message": FETCH_ITEM_FAILED,
            "error": str(e)
        }


def update_item(db: Session, item_id: int, data: dict):
    """
    Fully update an item.

    Args:
        db (Session):
            Active SQLAlchemy database session.

        item_id (int):
            Item ID.

        data (dict):
            Updated item payload.

    Returns:
        dict:
            Returns updated item or failure response.
    """

    try:
        item_response = get_item(db, item_id)

        if not item_response["success"]:
            return item_response

        item = item_response["data"]

        if "category_id" in data:
            if not db.query(Category).filter(
                Category.id == data["category_id"]
            ).first():
                return {
                    "success": False,
                    "message": INVALID_CATEGORY_ID
                }

        for key, value in data.items():
            setattr(item, key, value)

        db.commit()
        db.refresh(item)

        return {
            "success": True,
            "message": ITEM_UPDATED_SUCCESS,
            "data": item
        }

    except IntegrityError:
        db.rollback()

        return {
            "success": False,
            "message": ITEM_UPDATION_ERROR
        }

    except Exception as e:
        db.rollback()

        return {
            "success": False,
            "message": UPDATE_ITEM_FAILED,
            "error": str(e)
        }


def patch_item(db: Session, item_id: int, data: dict):
    """
    Partially update an item.

    Args:
        db (Session):
            Active SQLAlchemy database session.

        item_id (int):
            Item ID.

        data (dict):
            Partial item payload.

    Returns:
        dict:
            Returns patched item or failure response.
    """

    try:
        item_response = get_item(db, item_id)

        if not item_response["success"]:
            return item_response

        item = item_response["data"]

        for key, value in data.items():
            if value is not None:
                setattr(item, key, value)

        db.commit()
        db.refresh(item)

        return {
            "success": True,
            "message": ITEM_UPDATED_SUCCESS,
            "data": item
        }

    except IntegrityError:
        db.rollback()

        return {
            "success": False,
            "message": ITEM_UPDATION_ERROR
        }

    except Exception as e:
        db.rollback()

        return {
            "success": False,
            "message": PATCH_ITEM_FAILED,
            "error": str(e)
        }


def delete_item(db: Session, item_id: int):
    """
    Delete an item.

    Args:
        db (Session):
            Active SQLAlchemy database session.

        item_id (int):
            Item ID.

    Returns:
        dict:
            Returns deletion status response.
    """

    try:
        item_response = get_item(db, item_id)

        if not item_response["success"]:
            return item_response

        item = item_response["data"]

        db.delete(item)
        db.commit()

        return {
            "success": True,
            "message": ITEM_DELETED
        }

    except Exception as e:
        db.rollback()

        return {
            "success": False,
            "message": DELETE_ITEM_FAILED,
            "error": str(e)
        }


def get_low_stock(db: Session):
    """
    Retrieve items with low stock quantity.

    Args:
        db (Session):
            Active SQLAlchemy database session.

    Returns:
        dict:
            Returns low stock items or failure response.
    """

    try:
        items = db.query(Item).filter(
            Item.quantity <= Item.threshold
        ).all()

        if not items:
            return {
                "success": False,
                "message": NO_LOW_STOCK_ITEMS
            }

        return {
            "success": True,
            "message": LOW_STOCK_ITEMS_FETCHED_SUCCESS,
            "data": items
        }

    except Exception as e:
        return {
            "success": False,
            "message": FETCH_LOW_STOCK_ITEMS_FAILED,
            "error": str(e)
        }


def get_expiring_items(db: Session):
    """
    Retrieve items expiring within 7 days.

    Args:
        db (Session):
            Active SQLAlchemy database session.

    Returns:
        dict:
            Returns expiring items or failure response.
    """

    try:
        today = date.today()
        next_week = today + timedelta(days=7)

        items = db.query(Item).filter(
            Item.expiry_date >= today,
            Item.expiry_date <= next_week
        ).all()

        if not items:
            return {
                "success": False,
                "message": NO_EXPIRING_ITEMS_FOUND
            }

        return {
            "success": True,
            "message": EXPIRING_ITEMS_FETCHED_SUCCESS,
            "data": items
        }

    except Exception as e:
        return {
            "success": False,
            "message": FETCH_EXPIRING_ITEMS_FAILED,
            "error": str(e)
        }


def get_items_by_supplier(db: Session, supplier: str):
    """
    Retrieve items by supplier name.

    Args:
        db (Session):
            Active SQLAlchemy database session.

        supplier (str):
            Supplier name.

    Returns:
        dict:
            Returns supplier items or failure response.
    """

    try:
        items = db.query(Item).filter(
            Item.supplier.ilike(f"%{supplier}%")
        ).all()

        if not items:
            return {
                "success": False,
                "message": SUPPLIER_NOT_FOUND
            }

        return {
            "success": True,
            "message": SUPPLIER_ITEMS_FETCHED_SUCCESS,
            "data": items
        }

    except Exception as e:
        return {
            "success": False,
            "message": FETCH_SUPPLIER_ITEMS_FAILED,
            "error": str(e)
        }


def get_user_items(db: Session, user_id: int):
    """
    Retrieve items created by a specific user.

    Args:
        db (Session):
            Active SQLAlchemy database session.

        user_id (int):
            User ID.

    Returns:
        dict:
            Returns user items or failure response.
    """

    try:
        items = db.query(Item).filter(
            Item.created_by == user_id
        ).all()

        if not items:
            return {
                "success": False,
                "message": USER_ITEMS_NOT_FOUND
            }

        return {
            "success": True,
            "message": USER_ITEMS_FETCHED_SUCCESS,
            "data": items
        }

    except Exception as e:
        return {
            "success": False,
            "message": FETCH_USER_ITEMS_FAILED,
            "error": str(e)
        }


def get_items_by_category(db: Session, category_id: int):
    """
    Retrieve items under a category.

    Args:
        db (Session):
            Active SQLAlchemy database session.

        category_id (int):
            Category ID.

    Returns:
        dict:
            Returns category items or failure response.
    """
    try:
        category = db.query(Category).filter(
            Category.id == category_id
        ).first()

        if not category:
            return {
                "success": False,
                "message": CATEGORY_NOT_FOUND
            }

        items = db.query(Item).filter(
            Item.category_id == category_id
        ).all()

        return {
            "success": True,
            "message": CATEGORY_ITEMS_FETCHED_SUCCESS,
            "data": items
        }

    except Exception as e:
        return {
            "success": False,
            "message": FETCH_CATEGORY_ITEMS_FAILED,
            "error": str(e)
        }