from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from ..models import Category
from ..constants import *


def create_category(db: Session, data: dict):
    """
    Create a new category.

    This function:
    - Validates duplicate category names
    - Creates a new category
    - Stores the category in the database

    Args:
        db (Session):
            Active SQLAlchemy database session.

        data (dict):
            Category payload containing category details.

    Returns:
        dict:
            Returns success or failure response with category data.
    """

    try:
        name = data["name"].strip()

        existing = db.query(Category).filter(
            func.lower(Category.name) == name.lower()
        ).first()

        if existing:
            return {
                "success": False,
                "message": CATEGORY_EXISTS
            }

        category = Category(name=name)

        db.add(category)
        db.commit()
        db.refresh(category)

        return {
            "success": True,
            "message": CATEGORY_CREATED_SUCCESS,
            "data": {
                "id": category.id,
                "name": category.name
            }
        }

    except IntegrityError:
        db.rollback()

        return {
            "success": False,
            "message": CATEGORY_EXISTS
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
            "message": CREATE_CATEGORY_FAILED,
            "error": str(e)
        }


def get_categories(db: Session):
    """
    Retrieve all categories.

    Args:
        db (Session):
            Active SQLAlchemy database session.

    Returns:
        dict:
            Returns list of categories or failure response.
    """

    try:
        categories = db.query(Category).all()

        return {
            "success": True,
            "message": CATEGORIES_FETCHED_SUCCESS,
            "data": categories
        }

    except Exception as e:
        return {
            "success": False,
            "message": FETCH_CATEGORIES_FAILED,
            "error": str(e)
        }


def get_category(db: Session, category_id: int):
    """
    Retrieve a category by ID.

    Args:
        db (Session):
            Active SQLAlchemy database session.

        category_id (int):
            Category ID.

    Returns:
        dict:
            Returns category data or failure response.
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

        return {
            "success": True,
            "message": CATEGORY_FETCHED_SUCCESS,
            "data": category
        }

    except Exception as e:
        return {
            "success": False,
            "message": FETCH_CATEGORY_FAILED,
            "error": str(e)
        }


def update_category(db: Session, category_id: int, data: dict):
    """
    Fully update a category.

    Args:
        db (Session):
            Active SQLAlchemy database session.

        category_id (int):
            Category ID.

        data (dict):
            Updated category payload.

    Returns:
        dict:
            Returns updated category or failure response.
    """

    try:
        category_response = get_category(db, category_id)

        if not category_response["success"]:
            return category_response

        category = category_response["data"]

        if "name" in data:
            name = data["name"].strip()

            existing = db.query(Category).filter(
                func.lower(Category.name) == name.lower(),
                Category.id != category_id
            ).first()

            if existing:
                return {
                    "success": False,
                    "message": CATEGORY_EXISTS
                }

            category.name = name

        db.commit()
        db.refresh(category)

        return {
            "success": True,
            "message": CATEGORY_UPDATED_SUCCESS,
            "data": category
        }

    except Exception as e:
        db.rollback()

        return {
            "success": False,
            "message": UPDATE_CATEGORY_FAILED,
            "error": str(e)
        }


def patch_category(db: Session, category_id: int, data: dict):
    """
    Partially update a category.

    Args:
        db (Session):
            Active SQLAlchemy database session.

        category_id (int):
            Category ID.

        data (dict):
            Partial category payload.

    Returns:
        dict:
            Returns patched category or failure response.
    """

    try:
        category_response = get_category(db, category_id)

        if not category_response["success"]:
            return category_response

        category = category_response["data"]

        if "name" in data and data["name"] is not None:
            name = data["name"].strip()

            existing = db.query(Category).filter(
                func.lower(Category.name) == name.lower(),
                Category.id != category_id
            ).first()

            if existing:
                return {
                    "success": False,
                    "message": CATEGORY_EXISTS
                }

            category.name = name

        db.commit()
        db.refresh(category)

        return {
            "success": True,
            "message": CATEGORY_UPDATED_SUCCESS,
            "data": category
        }

    except Exception as e:
        db.rollback()

        return {
            "success": False,
            "message": PATCH_CATEGORY_FAILED,
            "error": str(e)
        }


def delete_category(db: Session, category_id: int):
    """
    Delete a category.

    Args:
        db (Session):
            Active SQLAlchemy database session.

        category_id (int):
            Category ID.

    Returns:
        dict:
            Returns deletion status response.
    """

    try:
        category_response = get_category(db, category_id)

        if not category_response["success"]:
            return category_response

        category = category_response["data"]

        db.delete(category)
        db.commit()

        return {
            "success": True,
            "message": CATEGORY_DELETED
        }

    except Exception as e:
        db.rollback()

        return {
            "success": False,
            "message": DELETE_CATEGORY_FAILED,
            "error": str(e)
        }