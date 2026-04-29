from .database import Base
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    items = relationship( "Item", back_populates="owner")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    items = relationship("Item", back_populates="category", cascade="all", passive_deletes=True)

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, default=0)
    threshold = Column(Integer, default=0)
    price = Column(Float, default=0.0)
    supplier = Column(String)
    expiry_date = Column(Date)
    category_id = Column(Integer,ForeignKey("categories.id", ondelete="CASCADE"),nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = relationship("Category", back_populates="items")
    owner = relationship("User", back_populates="items")