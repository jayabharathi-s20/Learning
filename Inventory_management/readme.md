pip install passlib[bcrypt] python-jose

passlib[bcrypt] → store passwords safely
python-jose → handle login tokens (JWT authentication)

----------------------------------------------------------
SECURITY.PY
----------------------------------------------------------
from passlib.context import CryptContext
    - You’re importing CryptContext from Passlib
    - This class manages how passwords are hashed and verified

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    Schemes=["bcrypt"]
        - Use bcrypt algorithm to hash passwords
    deprecated="auto"
        - If you later change algorithm, old hashes can still be handled safely

def hash_password(password: str) -> str:
    return pwd_context.hash(password)
        - Generates a random salt
        - Combines password + salt
        - Applies bcrypt hashing

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

        - User enters password at login:
            plain_password = "mypassword123"

        - You fetch stored hash from DB:
            hashed_password = "$2b$12$8sjdhf..."
        - verify() does internally:
            Extracts salt from stored hash
            Hashes input password using same method
            Compares results securely
        - Returns:
            True → correct password
            False → wrong password

----------------------------------------------------------
AUTH.PY
----------------------------------------------------------
from jose import JWTError, jwt
    - This is your JWT engine
    - jwt → used to:
        create token (encode)
        read token (decode)
    JWTError → used to:
        catch errors when token is invalid / expired / tampered

def create_access_token(data: dict) -> str:
    This function is used to generate a token when a user logs in. It takes user data (like user id), creates an expiry time, adds that expiry to the data, and then generates a JWT token using that data.

def decode_token(token: str):
    This function decodes and verifies the token sent by the user and returns the payload data to the backend for further processing.