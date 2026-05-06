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


def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Token not found")

    payload = decode_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

class Roles:
    ADMIN = "admin"
    MANAGER = "manager"
    STAFF = "staff"



class RequiredRoles:
    def __init__(self,*roles):
        self.roles=roles
        
    def __call__(self,user = Depends(get_current_user)):
        if not user.role:
            raise HTTPException(status_code=403, detail="Role not assigned")
        
        if user.role not in self.roles:
            raise HTTPException(status_code=403, detail="Access denied")

        return user
    
admin_only = RequiredRoles(Roles.ADMIN)

admin_manager = RequiredRoles(Roles.ADMIN, Roles.MANAGER)

all_roles = RequiredRoles(Roles.ADMIN, Roles.MANAGER, Roles.STAFF)