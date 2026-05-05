from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta
from app.models import User, Category, Item
from sqlalchemy.exc import IntegrityError
from app.utils.auth import create_access_token
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user):
    """
    Create a new user.

    - Checks if email already exists
    - Hashes the password before storing
    """
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise ValueError("Email already exists")

    hashed_pw = pwd_context.hash(user.password)

    db_user = User(
        name=user.name.strip(),
        email=user.email,
        password=hashed_pw
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def authenticate_user(db, email: str, password: str):
    """
    Authenticate a user using email and password.

    Returns:
        User | None
    """

    if not password or password.strip() == "":
        return None

    if len(password) > 128:
        return None

    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not pwd_context.verify(password, user.password):
        return None

    return user


def login_user(db, email: str, password: str):
    """
    Login user and generate JWT token.

    Args:
        db (Session): Database session
        email (str): User email
        password (str): Plain password

    Returns:
        dict | None: Token response or None if invalid
    """
    user = authenticate_user(db, email, password)

    if not user:
        return None

    token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


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
        data (dict): Updated data

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
        data (dict): Partial data

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
    Delete a user by ID.

    Args:
        db (Session): Database session
        user_id (int): User ID

    Returns:
        dict | None: Success message or None
    """
    user = get_user(db, user_id)
    if not user:
        return None

    db.delete(user)
    db.commit()
    return {"message": "User deleted"}


def create_category(db: Session, data: dict):
    """
    Create a new category.

    Args:
        db (Session): Database session
        data (dict): Category data

    Returns:
        Category: Created category

    Raises:
        ValueError: If category already exists
    """
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


def get_categories(db: Session):
    """
    Retrieve all categories.

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
    """
    Fully update a category.

    Returns:
        Category | None
    """
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
    """
    Partially update a category.

    Returns:
        Category | None
    """
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
    Create a new item
    """
    try:
        if not db.query(Category).filter(Category.id == data["category_id"]).first():
            raise ValueError("Invalid category_id")

        if not db.query(User).filter(User.id == data["created_by"]).first():
            raise ValueError("Invalid created_by")

        item = Item(**data)

        db.add(item)
        db.commit()
        db.refresh(item)

        return item

    except IntegrityError:
        db.rollback()
        raise ValueError("Error creating item")



def get_items(db: Session):
    """
    Get all items
    """
    return db.query(Item).all()


def get_item(db: Session, item_id: int):
    """
    Get single item by ID
    """
    return db.query(Item).filter(Item.id == item_id).first()



def update_item(db: Session, item_id: int, data: dict):
    """
    Fully update item
    """
    item = get_item(db, item_id)

    if not item:
        return None

    try:
        if "category_id" in data:
            if not db.query(Category).filter(Category.id == data["category_id"]).first():
                raise ValueError("Invalid category_id")

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
    Partially update item
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
    Delete item
    """
    item = get_item(db, item_id)

    if not item:
        return None

    db.delete(item)
    db.commit()

    return {"message": "Item deleted"}



def get_low_stock(db: Session):
    """
    Items where quantity <= threshold
    """
    return db.query(Item).filter(
        Item.quantity <= Item.threshold
    ).all()


def get_expiring_items(db: Session):
    """
    Items expiring within next 7 days
    """
    today = date.today()
    next_week = today + timedelta(days=7)

    return db.query(Item).filter(
        Item.expiry_date >= today,
        Item.expiry_date <= next_week
    ).all()


def get_items_by_supplier(db: Session, supplier: str):
    """
    Case-insensitive supplier search
    """
    return db.query(Item).filter(
        Item.supplier.ilike(f"%{supplier}%")
    ).all()


def get_user_items(db: Session, user_id: int):
    """
    Items created by specific user
    """
    return db.query(Item).filter(
        Item.created_by == user_id
    ).all()


def get_items_by_category(db: Session, category_id: int):
    """
    Items under a category
    """
    return db.query(Item).filter(
        Item.category_id == category_id
    ).all()
