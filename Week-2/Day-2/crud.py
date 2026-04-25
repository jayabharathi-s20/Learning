from sqlalchemy.orm import Session
from models import User

def create_user(db: Session, name: str, age: int):
    """Create a new user"""
    user = User(name=name, age=age)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_all_users(db: Session):
    """Get all the users"""
    return db.query(User).all()


def get_user(db: Session, user_id: int):
    """Getting single user with id"""
    return db.query(User).filter(User.id == user_id).first()

def update_full_user(db: Session, user_id: int, name: str, age: int):
    """update all the users --method(put)"""
    user = get_user(db, user_id)
    if user:
        user.name = name
        user.age = age
        db.commit()
        db.refresh(user)
    return user

def update_partial_user(db: Session, user_id: int, name: str, age: int):
    """update specific field of the users --method(patch)"""
    user = get_user(db, user_id)
    if user:
        if name is not None:
            user.name = name
        if age is not None:
            user.age = age
        db.commit()
        db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    """delete particular user with ref to id"""
    user = get_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()
    return user