from .models import Base
from .database import engine

Base.metadata.create_all(bind=engine)
# Base.metadata.drop_all(bind=engine)
