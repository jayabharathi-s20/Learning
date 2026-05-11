from ..utils.dependencies import  get_db
from ..utils.security import create_access_token, decode_token
from ..models import UserCreate, LoginSchema
from fastapi import APIRouter, Depends, HTTPException, Response, Request,status
from sqlalchemy.orm import Session
from ..controllers import auth_controllers
from ..constants import *


router = APIRouter()

@router.post("/register",status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    try:
        created_user= auth_controllers.create_user(db, user)
        return created_user
    
    except HTTPException:
        raise
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error_code": "REGISTRATION_FAILED",
                "message": str(e)
            }
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error_code": "INTERNAL_SERVER_ERROR",
                "message": INTERNAL_SERVER_ERROR
            }
        )
    


@router.post("/login",status_code=status.HTTP_200_OK)
def login(data: LoginSchema, response: Response, db: Session = Depends(get_db)):
    """
    Authenticate user and generate tokens.
    """
    try:
        result = auth_controllers.login_user(db, data.email, data.password)

        if not result:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail={"success": False,
                                        "error_code": "INVALID_CREDENTIALS",
                                        "message": INVALID_CREDENTIALS})

        response.set_cookie(
            "access_token",
            result["data"]["access_token"],
            httponly=True,
            samesite="lax"
        )

        response.set_cookie(
            "refresh_token",
            result["data"]["refresh_token"],
            httponly=True,
            samesite="lax"
        )

        return result
    
    except HTTPException:
        raise

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail={"success": False,
                                    "error_code": "VALIDATION_ERROR",
                                    "message": str(e)})
    
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error_code": "LOGIN_FAILED",
                "message": INTERNAL_SERVER_ERROR
            }
        )

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(response: Response):
    """
    Logout user and clear authentication cookies.
    """
    try:
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return {"success":True,"message": LOGOUT_SUCCESS}
    except Exception:        
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"success": False,"error_code": "LOGOUT_FAILED","message": INTERNAL_SERVER_ERROR})


@router.post("/refresh",status_code=status.HTTP_200_OK)
def refresh_token(request: Request, response: Response):
    """
    Generate a new access token using refresh token.
    """
    try:
        token = request.cookies.get("refresh_token")

        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "success": False,
                    "error_code": "MISSING_REFRESH_TOKEN",
                    "message": MISSING_REFRESH_TOKEN
                }
            )


        payload = decode_token(token)

        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "success": False,
                    "error_code": "INVALID_REFRESH_TOKEN",
                    "message": INVALID_REFRESH_TOKEN
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

        new_access_token = create_access_token({"sub": user_id})

        response.set_cookie("access_token", new_access_token, httponly=True, samesite="lax")

        return {"success": True,"message": ACCESS_TOKEN_REFRESHED}
    
    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error_code": "TOKEN_REFRESH_FAILED",
                "message": INTERNAL_SERVER_ERROR
            }
        )
