from pydantic import BaseModel, Field
from datetime import date

class Item(BaseModel):
    item_id: int
    name: str
    quantity: int = Field(ge=0)
    threshold: int = Field(ge=0)
    price: float = Field(gt=0)
    category: str
    supplier: str
    expiry_date: date

#Item(...) = core data safety (Pydantic layer)
# validator.py (if you made one) = business/custom logic layer