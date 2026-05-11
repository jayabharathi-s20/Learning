from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..models import User
from ..utils.security import create_access_token, create_refresh_token
from passlib.context import CryptContext
from ..constants import *

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user):
    """
    Create a new user account.

    This function:
    - Checks whether the email already exists
    - Hashes the password securely
    - Stores the user in the database

    Args:
        db (Session):
            Active SQLAlchemy database session.

        user:
            User registration payload.

    Returns:
        dict:
            Returns success or failure response with message and user data.
    """
    try:
        existing = db.query(User).filter(User.email == user.email).first()

        if existing:
            return {
                "success": False,
                "message": EMAIL_EXISTS
            }

        hashed_pw = pwd_context.hash(user.password)

        db_user = User(
            name=user.name.strip(),
            email=user.email,
            password=hashed_pw,
            role=user.role
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return {
            "success": True,
            "message": USER_CREATED_SUCCESS,
            "data": {
                "id": db_user.id,
                "name": db_user.name,
                "email": db_user.email,
                "role": db_user.role
            }
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
            "message": SOMETHING_WENT_WRONG,
            "error": str(e)
        }


def authenticate_user(db: Session, email: str, password: str):
    """
    Authenticate a user using email and password.

    This function validates:
    - Empty password
    - Password length
    - Existing user
    - Password correctness

    Args:
        db (Session):
            Active SQLAlchemy database session.

        email (str):
            User email address.

        password (str):
            Plain text password.

    Returns:
        dict:
            Returns authentication status with user object or error message.
    """

    try:
        if not password or password.strip() == "":
            return {
                "success": False,
                "message": PASSWORD_REQUIRED
            }

        if len(password) > 128:
            return {
                "success": False,
                "message": INVALID_PASSWORD
            }

        user = db.query(User).filter(User.email == email).first()

        if not user:
            return {
                "success": False,
                "message": USER_NOT_FOUND
            }

        if not pwd_context.verify(password, user.password):
            return {
                "success": False,
                "message": INVALID_CREDENTIALS
            }

        return {
            "success": True,
            "user": user
        }

    except Exception as e:
        return {
            "success": False,
            "message": SOMETHING_WENT_WRONG,
            "error": str(e)
        }


def login_user(db: Session, email: str, password: str):
    """
    Login user and generate JWT tokens.

    This function:
    - Authenticates the user
    - Generates access token
    - Generates refresh token

    Args:
        db (Session):
            Active SQLAlchemy database session.

        email (str):
            User email address.

        password (str):
            Plain text password.

    Returns:
        dict:
            Returns login status, JWT tokens, and user role.
    """

    try:
        auth_response = authenticate_user(db, email, password)

        if not auth_response["success"]:
            return auth_response

        user = auth_response["user"]

        access_token = create_access_token({
            "sub": str(user.id),
            "role": user.role
        })

        refresh_token = create_refresh_token({
            "sub": str(user.id)
        })

        return {
            "success": True,
            "message": LOGIN_SUCCESS,
            "data": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "role": user.role
            }
        }

    except Exception as e:
        return {
            "success": False,
            "message": SOMETHING_WENT_WRONG,
            "error": str(e)
        }