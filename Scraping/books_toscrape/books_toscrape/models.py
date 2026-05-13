from sqlalchemy import Column, Integer, String,Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base

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
    host_url = Column(String(255))
    title = Column(String(255))
    price = Column(String(50))
    product_information = Column(JSONB)
    image_url = Column(String(500))
    stock = Column(String(100))
    pagination_url=Column(String(500))



   