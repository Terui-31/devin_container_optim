"""
Unit tests for the FastAPI application endpoints.

Tests cover health check, item retrieval, and optimization endpoints
with various scenarios including error cases.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

backend_path = os.path.join(project_root, 'backend')
sys.path.insert(0, backend_path)

from sqlmodel import SQLModel
SQLModel.metadata.clear()

from backend.main import app, get_session
from backend.models import ItemCatalog


@pytest.fixture(name="session")
def session_fixture():
    """Create a test database session."""
    engine = create_engine(
        "sqlite://", 
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        test_items = [
            ItemCatalog(
                sku="TEST001",
                name="Test Box A",
                length=30.0,
                width=20.0,
                height=15.0,
                weight=2.5
            ),
            ItemCatalog(
                sku="TEST002", 
                name="Test Box B",
                length=50.0,
                width=40.0,
                height=30.0,
                weight=8.0
            ),
            ItemCatalog(
                sku="TEST003",
                name="Test Box C", 
                length=15.0,
                width=10.0,
                height=8.0,
                weight=0.8
            )
        ]
        for item in test_items:
            session.add(item)
        session.commit()
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create a test client with dependency override."""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


class TestHealthEndpoint:
    """Test cases for the health check endpoint."""
    
    def test_health_check_returns_200(self, client: TestClient):
        """Test that health check endpoint returns 200 OK."""
        response = client.get("/healthz")
        assert response.status_code == 200
        assert response.json() == {
            "status": "OK",
            "message": "Container Loading Optimizer API is running"
        }


class TestItemsEndpoints:
    """Test cases for item catalog endpoints."""
    
    def test_list_items_returns_all_items(self, client: TestClient):
        """Test that list items endpoint returns all catalog items."""
        response = client.get("/items")
        assert response.status_code == 200
        items = response.json()
        assert len(items) == 3
        assert all("sku" in item for item in items)
        assert all("name" in item for item in items)
    
    def test_get_item_by_sku_success(self, client: TestClient):
        """Test successful item retrieval by SKU."""
        response = client.get("/items/TEST001")
        assert response.status_code == 200
        item = response.json()
        assert item["sku"] == "TEST001"
        assert item["name"] == "Test Box A"
        assert item["length"] == 30.0
        assert item["width"] == 20.0
        assert item["height"] == 15.0
        assert item["weight"] == 2.5
    
    def test_get_item_by_sku_not_found(self, client: TestClient):
        """Test item retrieval with non-existent SKU."""
        response = client.get("/items/NONEXISTENT")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


class TestOptimizeEndpoint:
    """Test cases for the optimization endpoint."""
    
    def test_optimize_perfect_fit_scenario(self, client: TestClient):
        """Test optimization with perfect fit scenario."""
        request_data = {
            "container": {
                "length": 60.0,
                "width": 40.0,
                "height": 30.0
            },
            "sku": "TEST001",
            "item_volume_margin": 1.0
        }
        
        response = client.post("/optimize", json=request_data)
        assert response.status_code == 200
        
        result = response.json()
        assert "max_count" in result
        assert "leftover_percentage" in result
        assert "container_volume" in result
        assert "item_volume" in result
        assert "item_details" in result
        
        assert result["max_count"] == 8
        assert result["leftover_percentage"] == 0.0
        assert result["container_volume"] == 72000.0
        assert result["item_volume"] == 9000.0
        assert result["item_details"]["sku"] == "TEST001"
    
    def test_optimize_acceptable_surplus(self, client: TestClient):
        """Test optimization with acceptable surplus (<10%)."""
        request_data = {
            "container": {
                "length": 20.0,
                "width": 10.0,
                "height": 10.0
            },
            "sku": "TEST003",
            "item_volume_margin": 0.95
        }
        
        response = client.post("/optimize", json=request_data)
        assert response.status_code == 200
        
        result = response.json()
        assert result["max_count"] > 0
        assert result["leftover_percentage"] < 10.0
    
    def test_optimize_inefficient_packing_error(self, client: TestClient):
        """Test optimization that results in inefficient packing (>10% leftover)."""
        request_data = {
            "container": {
                "length": 100.0,
                "width": 100.0,
                "height": 100.0
            },
            "sku": "TEST001",
            "item_volume_margin": 0.95
        }
        
        response = client.post("/optimize", json=request_data)
        assert response.status_code == 422
        assert "Inefficient packing" in response.json()["detail"]
    
    def test_optimize_item_too_large_error(self, client: TestClient):
        """Test optimization where item dimensions exceed container."""
        request_data = {
            "container": {
                "length": 10.0,
                "width": 10.0,
                "height": 10.0
            },
            "sku": "TEST002"  # 50x40x30 item won't fit in 10x10x10 container
        }
        
        response = client.post("/optimize", json=request_data)
        assert response.status_code == 422
        assert "larger than container" in response.json()["detail"]
    
    def test_optimize_item_not_found_error(self, client: TestClient):
        """Test optimization with non-existent SKU."""
        request_data = {
            "container": {
                "length": 60.0,
                "width": 40.0,
                "height": 30.0
            },
            "sku": "NONEXISTENT"
        }
        
        response = client.post("/optimize", json=request_data)
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
    
    def test_optimize_invalid_container_dimensions(self, client: TestClient):
        """Test optimization with invalid container dimensions."""
        request_data = {
            "container": {
                "length": -10.0,  # Invalid negative dimension
                "width": 40.0,
                "height": 30.0
            },
            "sku": "TEST001"
        }
        
        response = client.post("/optimize", json=request_data)
        assert response.status_code == 422  # Validation error
    
    def test_optimize_custom_volume_margin(self, client: TestClient):
        """Test optimization with custom volume margin."""
        request_data = {
            "container": {
                "length": 60.0,
                "width": 40.0,
                "height": 30.0
            },
            "sku": "TEST001",
            "item_volume_margin": 0.8
        }
        
        response = client.post("/optimize", json=request_data)
        assert response.status_code == 200
        
        result = response.json()
        assert result["max_count"] > 0
        assert result["leftover_percentage"] > 0.0


class TestAPIDocumentation:
    """Test cases for API documentation endpoints."""
    
    def test_openapi_docs_accessible(self, client: TestClient):
        """Test that OpenAPI documentation is accessible."""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_redoc_docs_accessible(self, client: TestClient):
        """Test that ReDoc documentation is accessible."""
        response = client.get("/redoc")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_openapi_json_schema(self, client: TestClient):
        """Test that OpenAPI JSON schema is accessible."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert schema["info"]["title"] == "Container Loading Optimizer API"
