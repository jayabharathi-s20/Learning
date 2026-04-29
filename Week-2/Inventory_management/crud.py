from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta
from .models import User, Category, Item
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func


def create_user(db: Session, data: dict):
    """
    Create a new user.

    Args:
        db (Session): Database session
        data (dict): User data (name, email)

    Returns:
        User: Created user object

    Raises:
        ValueError: If email already exists
    """
    try:
        user = User(**data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise ValueError("Email already exists")
    

def get_users(db: Session):
    """
    Retrieve all users.

    Args:
        db (Session): Database session

    Returns:
        List[User]: List of users
    """
    return db.query(User).all()


def get_user(db: Session, user_id: int):
    """
    Retrieve a user by ID.

    Args:
        db (Session): Database session
        user_id (int): User ID

    Returns:
        User | None: User object or None if not found
    """
    return db.query(User).filter(User.id == user_id).first()


def update_user(db: Session, user_id: int, data: dict):
    """
    Fully update a user.

    Args:
        db (Session): Database session
        user_id (int): User ID
        data (dict): Updated user data

    Returns:
        User | None: Updated user or None if not found

    Raises:
        ValueError: If email already exists
    """
    user = get_user(db, user_id)
    if not user:
        return None

    try:
        if "email" in data:
            existing = db.query(User).filter(
                User.email == data["email"],
                User.id != user_id
            ).first()

            if existing:
                raise ValueError("Email already exists")

        for key, value in data.items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return user

    except IntegrityError:
        db.rollback()
        raise ValueError("Email already exists")


def patch_user(db: Session, user_id: int, data: dict):
    """
    Partially update a user.

    Args:
        db (Session): Database session
        user_id (int): User ID
        data (dict): Partial update data

    Returns:
        User | None: Updated user or None

    Raises:
        ValueError: If email already exists
    """
    user = get_user(db, user_id)
    if not user:
        return None

    try:
        if "email" in data:
            existing = db.query(User).filter(
                User.email == data["email"],
                User.id != user_id
            ).first()

            if existing:
                raise ValueError("Email already exists")

        for key, value in data.items():
            if value is not None:
                setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return user

    except IntegrityError:
        db.rollback()
        raise ValueError("Email already exists")


def delete_user(db: Session, user_id: int):
    """
    Delete a user.

    Args:
        db (Session): Database session
        user_id (int): User ID

    Returns:
        dict | None: Success message or None if user not found
    """
    user = get_user(db, user_id)
    if not user:
        return None

    db.delete(user)
    db.commit()
    return {"message": "User deleted"}


def create_category(db: Session, data: dict):
    try:
        name = data["name"].strip() 

        existing = db.query(Category).filter(
            func.lower(Category.name) == name.lower()
        ).first()

        if existing:
            raise ValueError("Category already exists")

        category = Category(name=name)  
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    except IntegrityError:
        db.rollback()
        raise ValueError("Category already exists")

def get_items_by_supplier(db: Session, supplier: str):
    """
    Filter items by supplier (case insensitive)
    """
    return db.query(Item).filter(
        Item.supplier.ilike(f"%{supplier}%")
    ).all()

def get_categories(db: Session):
    """
    Retrieve all categories.

    Args:
        db (Session): Database session

    Returns:
        List[Category]
    """
    return db.query(Category).all()


def get_category(db: Session, category_id: int):
    """
    Retrieve category by ID.

    Returns:
        Category | None
    """
    return db.query(Category).filter(Category.id == category_id).first()


def update_category(db: Session, category_id: int, data: dict):
    category = get_category(db, category_id)
    if not category:
        return None

    if "name" in data:
        name = data["name"].strip()

        existing = db.query(Category).filter(
            func.lower(Category.name) == name.lower(),
            Category.id != category_id
        ).first()

        if existing:
            raise ValueError("Category already exists")

        category.name = name  

    db.commit()
    db.refresh(category)
    return category


def patch_category(db: Session, category_id: int, data: dict):
    category = get_category(db, category_id)
    if not category:
        return None

    if "name" in data and data["name"] is not None:
        name = data["name"].strip()

        existing = db.query(Category).filter(
            func.lower(Category.name) == name.lower(),
            Category.id != category_id
        ).first()

        if existing:
            raise ValueError("Category already exists")

        category.name = name  

    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int):
    """
    Delete a category.

    Returns:
        dict | None
    """
    category = get_category(db, category_id)
    if not category:
        return None

    db.delete(category)
    db.commit()
    return {"message": "Category deleted"}

def create_item(db: Session, data: dict):
    """
    Create a new item.

    Returns:
        Item

    Raises:
        ValueError: If invalid category/user
    """
    try:
        if not db.query(Category).filter(Category.id == data["category_id"]).first():
            raise ValueError("Invalid category_id")
        

        if not db.query(User).filter(User.id == data["created_by"]).first():
            raise ValueError("Invalid created_by (user not found)")

        item = Item(**data)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    except IntegrityError:
        db.rollback()
        raise ValueError("Error creating item")


def get_items(db: Session):
    """Return all items."""
    return db.query(Item).all()


def get_item(db: Session, item_id: int):
    """Return item by ID."""
    return db.query(Item).filter(Item.id == item_id).first()


def update_item(db: Session, item_id: int, data: dict):
    """
    Fully update an item.

    Returns:
        Item | None
    """
    item = get_item(db, item_id)
    if not item:
        return None

    try:
        if "category_id" in data:
            if not db.query(Category).filter(Category.id == data["category_id"]).first():
                raise ValueError("Invalid category_id")

        if "created_by" in data:
            if not db.query(User).filter(User.id == data["created_by"]).first():
                raise ValueError("Invalid created_by")

        for key, value in data.items():
            setattr(item, key, value)

        db.commit()
        db.refresh(item)
        return item

    except IntegrityError:
        db.rollback()
        raise ValueError("Error updating item")


def patch_item(db: Session, item_id: int, data: dict):
    """
    Partially update an item.

    Returns:
        Item | None
    """
    item = get_item(db, item_id)
    if not item:
        return None

    try:
        for key, value in data.items():
            if value is not None:
                setattr(item, key, value)

        db.commit()
        db.refresh(item)
        return item

    except IntegrityError:
        db.rollback()
        raise ValueError("Error updating item")


def delete_item(db: Session, item_id: int):
    """
    Delete an item.

    Returns:
        dict | None
    """
    item = get_item(db, item_id)
    if not item:
        return None

    db.delete(item)
    db.commit()
    return {"message": "Item deleted"}

def get_low_stock(db: Session):
    """
    Get items where quantity <= threshold
    """
    return db.query(Item).filter(
        Item.quantity <= Item.threshold
    ).all()

def get_expiring_items(db: Session):
    """
    Items expiring in next 7 days
    """
    today = date.today()
    next_week = today + timedelta(days=7)

    return db.query(Item).filter(
        Item.expiry_date >= today,
        Item.expiry_date <= next_week
    ).all()

def get_items_by_supplier(db: Session, supplier: str):
    """
    Filter items by supplier (case insensitive)
    """
    return db.query(Item).filter(
        Item.supplier.ilike(f"%{supplier}%")
    ).all()

def get_user_items(db: Session, user_id: int):
    return db.query(Item).filter(
        Item.created_by == user_id
    ).all()

def get_items_by_category(db: Session, category_id: int):
    return db.query(Item).filter(
        Item.category_id == category_id
    ).all()