"""
FastAPI application for container loading optimization.

This module provides REST API endpoints for calculating optimal container loading
configurations using the mathematical optimization algorithms.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import Dict, Tuple
from pydantic import BaseModel, Field

from database import engine
from models import ItemCatalog
from optimizer import maximize_load


app = FastAPI(
    title="Container Loading Optimizer API",
    description="REST API for calculating optimal container loading configurations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ContainerDimensions(BaseModel):
    """Container dimensions model for API requests."""
    length: float = Field(gt=0, description="Container length in cm")
    width: float = Field(gt=0, description="Container width in cm") 
    height: float = Field(gt=0, description="Container height in cm")


class OptimizeRequest(BaseModel):
    """Request model for optimization endpoint."""
    container: ContainerDimensions
    sku: str = Field(description="SKU of the item to optimize")
    item_volume_margin: float = Field(default=0.95, ge=0.1, le=1.0, description="Volume utilization margin (0.1-1.0)")


class OptimizeResponse(BaseModel):
    """Response model for optimization endpoint."""
    max_count: int = Field(description="Maximum number of items that can be loaded")
    leftover_percentage: float = Field(description="Percentage of unused container space")
    container_volume: float = Field(description="Total container volume in cm³")
    item_volume: float = Field(description="Individual item volume in cm³")
    item_details: Dict = Field(description="Item information from catalog")


def get_session():
    """Dependency to get database session."""
    with Session(engine) as session:
        yield session


@app.get("/healthz", status_code=200)
async def health_check():
    """Health check endpoint."""
    return {"status": "OK", "message": "Container Loading Optimizer API is running"}


@app.get("/items", response_model=list[ItemCatalog])
async def list_items(session: Session = Depends(get_session)):
    """List all available items in the catalog."""
    items = session.exec(select(ItemCatalog)).all()
    return items


@app.get("/items/{sku}", response_model=ItemCatalog)
async def get_item(sku: str, session: Session = Depends(get_session)):
    """Get item details by SKU."""
    item = session.exec(select(ItemCatalog).where(ItemCatalog.sku == sku)).first()
    if not item:
        raise HTTPException(status_code=404, detail=f"Item with SKU '{sku}' not found")
    return item


@app.post("/optimize", response_model=OptimizeResponse)
async def optimize_container_loading(
    request: OptimizeRequest,
    session: Session = Depends(get_session)
):
    """
    Calculate optimal container loading configuration.
    
    This endpoint takes container dimensions and an item SKU, then calculates
    the maximum number of items that can be loaded while maintaining efficiency
    constraints (leftover space ≤ 10%).
    """
    item = session.exec(select(ItemCatalog).where(ItemCatalog.sku == request.sku)).first()
    if not item:
        raise HTTPException(status_code=404, detail=f"Item with SKU '{request.sku}' not found")
    
    container_dim = (request.container.length, request.container.width, request.container.height)
    item_dim = (item.length, item.width, item.height)
    
    try:
        result = maximize_load(
            container_dim=container_dim,
            item_dim=item_dim,
            item_volume_margin=request.item_volume_margin
        )
        
        container_volume = container_dim[0] * container_dim[1] * container_dim[2]
        item_volume = item_dim[0] * item_dim[1] * item_dim[2]
        
        return OptimizeResponse(
            max_count=result["max_count"],
            leftover_percentage=result["leftover_percentage"],
            container_volume=container_volume,
            item_volume=item_volume,
            item_details={
                "sku": item.sku,
                "name": item.name,
                "dimensions": {
                    "length": item.length,
                    "width": item.width,
                    "height": item.height
                },
                "weight": item.weight
            }
        )
        
    except ValueError as e:
        if "Inefficient packing" in str(e):
            raise HTTPException(
                status_code=422,
                detail=f"Inefficient packing configuration: {str(e)}"
            )
        elif "Item dimensions exceed container dimensions" in str(e):
            raise HTTPException(
                status_code=422,
                detail="Item dimensions are larger than container dimensions"
            )
        else:
            raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
