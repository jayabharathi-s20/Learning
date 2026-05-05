from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.utils.auth import decode_token



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(request: Request,
db: Session = Depends(get_db)
):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(401, "Missing token")

    payload = decode_token(token)

    if not payload:
        raise HTTPException(401, "Invalid token")

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(401, "Invalid token payload")

    try:
        user_id = int(user_id)
    except:
        raise HTTPException(401, "Invalid token data")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(401, "User not found")

    return user