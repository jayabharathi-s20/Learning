from database import Base
from sqlalchemy import Integer, String, Column

class User(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=True)

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', age={self.age})"