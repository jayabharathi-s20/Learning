from fastapi import Request, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.connections import SessionLocal
from app.models import User
from ..utils.security import decode_token
from ..constants import *


def get_db():
    """
    Create and provide a database session.

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Retrieve the currently authenticated user.

    Workflow:
    - Read access token from cookies
    - Decode JWT token
    - Extract user ID from payload
    - Fetch user from database

    Args:
        request (Request): FastAPI request object
        db (Session): Database session

    Returns:
        User: Authenticated user object

    Raises:
        HTTPException:
            - 401 if token is missing
            - 401 if token is invalid
            - 401 if payload is invalid
            - 401 if user does not exist
    """
    try:
        token = request.cookies.get("access_token")

        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "success": False,
                    "error_code": "TOKEN_NOT_FOUND",
                    "message": TOKEN_NOT_FOUND
                }
            )

        payload = decode_token(token)

        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "success": False,
                    "error_code": "INVALID_TOKEN",
                    "message": INVALID_TOKEN
                }
            )

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "success": False,
                    "error_code": "INVALID_TOKEN_PAYLOAD",
                    "message": INVALID_TOKEN_PAYLOAD
                }
            )

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "success": False,
                    "error_code": "USER_NOT_FOUND",
                    "message": USER_NOT_FOUND
                }
            )

        return user

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error_code": "AUTHENTICATION_FAILED",
                "message": INTERNAL_SERVER_ERROR
            }
        )


class Roles:
    """
    Available application roles.
    """

    ADMIN = "admin"
    MANAGER = "manager"
    STAFF = "staff"


class RequiredRoles:
    """
    Role-based access control dependency.

    Usage:
        Depends(RequiredRoles("admin"))

    Args:
        *roles: Allowed roles
    """

    def __init__(self, *roles):
        self.roles = roles

    def __call__(
        self,
        user=Depends(get_current_user)
    ):
        """
        Validate user role permissions.

        Args:
            user (User): Authenticated user

        Returns:
            User: Authorized user object

        Raises:
            HTTPException:
                - 403 if role is missing
                - 403 if access is denied
        """
        try:
            if not user.role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={
                        "success": False,
                        "error_code": "ROLE_NOT_ASSIGNED",
                        "message": ROLE_NOT_ASSIGNED
                    }
                )

            if user.role not in self.roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={
                        "success": False,
                        "error_code": "ACCESS_DENIED",
                        "message": ACCESS_DENIED
                    }
                )

            return user

        except HTTPException:
            raise

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "success": False,
                    "error_code": "ROLE_VALIDATION_FAILED",
                    "message": INTERNAL_SERVER_ERROR
                }
            )


admin_only = RequiredRoles(Roles.ADMIN)

admin_manager = RequiredRoles(
    Roles.ADMIN,
    Roles.MANAGER
)

all_roles = RequiredRoles(
    Roles.ADMIN,
    Roles.MANAGER,
    Roles.STAFF
)