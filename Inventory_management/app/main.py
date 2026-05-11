from fastapi import FastAPI

from app.routes.auth_routes import router as auth
from app.routes.user_routes import router as users
from app.routes.items_routes import router as items
from app.routes.category_routes import router as category


app = FastAPI()

app.include_router(auth)
app.include_router(users)
app.include_router(category)
app.include_router(items)
