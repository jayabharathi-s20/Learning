from sqlalchemy import Column, Integer, String,Text,DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base
from datetime import datetime
from zoneinfo import ZoneInfo

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    host_url = Column(String(255))
    title = Column(String(255))
    price = Column(String(50))
    description = Column(Text)
    image_url = Column(String(500))
    stock = Column(String(100))
    product_information = Column(String)  

class Pagination(Base):
    __tablename__ = "pagination"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category=Column(String(255))
    host_url = Column(String(255),unique=True)
    title = Column(String(255))
    price = Column(String(50))
    description = Column(Text)
    product_information = Column(String)
    image_url = Column(String(500))
    stock = Column(String(100))
    pagination_url=Column(String(500))
    # # created_at=Column(DateTime,default=datetime.UTC)
    # created_at=Column(DateTime(timezone=True),default=lambda: datetime.now(ZoneInfo("Asia/Kolkata")))
    # updated_at = Column(DateTime(timezone=True),default=lambda: datetime.now(ZoneInfo("Asia/Kolkata")))
    # created_at = Column(DateTime, default=datetime.utcnow)
    # updated_at = Column(DateTime, default=datetime.utcnow,onupdate=datetime.utcnow)

    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)



   