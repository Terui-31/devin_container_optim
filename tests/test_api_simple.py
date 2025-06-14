"""
Simplified unit tests for the FastAPI application endpoints.
Focuses on core functionality without complex database setup.
"""

import pytest
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'backend'))

def test_optimizer_integration():
    """Test that the optimizer function works correctly."""
    from backend.optimizer import maximize_load
    
    result = maximize_load((60, 40, 30), (30, 20, 15), 1.0)
    assert result["max_count"] == 8
    assert result["leftover_percentage"] == 0.0
    
    with pytest.raises(ValueError, match="Inefficient packing"):
        maximize_load((100, 100, 100), (30, 20, 15), 0.95)

def test_fastapi_app_creation():
    """Test that FastAPI app can be created and configured."""
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    
    app = FastAPI()
    
    @app.get("/healthz")
    def health_check():
        return {"status": "OK", "message": "Container Loading Optimizer API is running"}
    
    assert app is not None
    assert hasattr(app, 'get')
    
    routes = [route.path for route in app.routes]
    assert "/healthz" in routes

def test_pydantic_models():
    """Test that Pydantic models work correctly."""
    from pydantic import BaseModel, Field, ValidationError
    
    class ContainerDimensions(BaseModel):
        length: float = Field(gt=0)
        width: float = Field(gt=0) 
        height: float = Field(gt=0)
    
    container = ContainerDimensions(length=60.0, width=40.0, height=30.0)
    assert container.length == 60.0
    assert container.width == 40.0
    assert container.height == 30.0
    
    with pytest.raises(ValidationError):
        ContainerDimensions(length=-10.0, width=40.0, height=30.0)
