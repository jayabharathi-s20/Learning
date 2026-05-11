from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

from ..constants import *


load_dotenv()

SECRET_KEY = os.getenv("secret_key")
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7


if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in environment variables")


def create_access_token(data: dict) -> str:
    """
    Create JWT access token.

    Args:
        data (dict): Token payload data

    Returns:
        str: Encoded JWT accesREFRESH_TOKEN_EXPIRE_DAYSs token

    Raises:
        ValueError: If token creation fails
    """
    try:
        to_encode = data.copy()

        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

        to_encode.update({
            "exp": expire,
            "type": "access"
        })

        encoded_jwt = jwt.encode(
            to_encode,
            SECRET_KEY,
            algorithm=ALGORITHM
        )

        return encoded_jwt

    except Exception as e:
        raise ValueError(
            f"{TOKEN_CREATE_ERROR}: {str(e)}"
        )


def create_refresh_token(data: dict) -> str:
    """
    Create JWT refresh token.

    Args:
        data (dict): Token payload data

    Returns:
        str: Encoded JWT refresh token

    Raises:
        ValueError: If refresh token creation fails
    """
    try:
        to_encode = data.copy()

        expire = datetime.utcnow() + timedelta(
            days=REFRESH_TOKEN_EXPIRE_DAYS
        )

        to_encode.update({
            "exp": expire,
            "type": "refresh"
        })

        encoded_jwt = jwt.encode(
            to_encode,
            SECRET_KEY,
            algorithm=ALGORITHM
        )

        return encoded_jwt

    except Exception as e:
        raise ValueError(
            f"{REFRESH_TOKEN_CREATE_ERROR}: {str(e)}"
        )


def decode_token(token: str):
    """
    Decode JWT token.

    Args:
        token (str): JWT token

    Returns:
        dict | None:
            - Decoded payload if valid
            - None if token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        return None

    except Exception:
        return None