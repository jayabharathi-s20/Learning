from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import session_creation
import crud

app = FastAPI()

def get_db():
    """Create and provide a database session, and close it after the request."""
    db = session_creation()
    try:
        yield db
    finally:
        db.close()

@app.post("/users")
def create_user(name: str, age: int, db: Session = Depends(get_db)):
    """
    Create new user

    Args:
        name (str): name of user
        age (int): age of the user
    """
    try:
        return crud.create_user(db, name, age)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users")
def read_users(db: Session = Depends(get_db)):
    """
    Get list of all users from the database
    """
    try:
        return crud.get_all_users(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get specific user by their id from db

    Args:
        user_id (int): ID of the user
    """
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/users/{user_id}")
def update_user(user_id: int, name: str, age: int, db: Session = Depends(get_db)):
    """
    Update all fields of a user (full update using PUT)

    Args:
        user_id (int): ID of the user
        name (str): Updated name
        age (int): Updated age
    """
    try:
        user = crud.update_full_user(db, user_id, name, age)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/users/{user_id}")
def patch_user(user_id: int, name: str = None, age: int = None, db: Session = Depends(get_db)):
    """
    Update only provided fields of a user (partial update using PATCH)

    Args:
        user_id (int): ID of the user
        name (str): Updated name (optional)
        age (int): Updated age (optional)
    """
    try:
        user = crud.update_partial_user(db, user_id, name, age)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user by their ID
    """
    try:
        user = crud.delete_user(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))