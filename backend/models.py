from sqlmodel import SQLModel, Field
from typing import Optional


class ItemCatalog(SQLModel, table=True):
    """
    Item catalog table for storing product information.
    
    This table stores the physical dimensions and weight of items
    that can be loaded into containers for optimization calculations.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    sku: str = Field(index=True, unique=True, description="Stock Keeping Unit - unique identifier")
    name: str = Field(description="Human-readable name of the item")
    length: float = Field(gt=0, description="Length of the item in cm")
    width: float = Field(gt=0, description="Width of the item in cm") 
    height: float = Field(gt=0, description="Height of the item in cm")
    weight: float = Field(gt=0, description="Weight of the item in kg")
    
    class Config:
        schema_extra = {
            "example": {
                "sku": "SKU001",
                "name": "Standard Box A",
                "length": 30.0,
                "width": 20.0,
                "height": 15.0,
                "weight": 2.5
            }
        }
