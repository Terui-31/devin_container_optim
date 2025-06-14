"""
Unit tests for the container loading optimizer module.

Tests cover various scenarios including perfect fit, acceptable surplus,
and cases that should raise exceptions for inefficient packing.
"""

import pytest
from backend.optimizer import maximize_load


class TestMaximizeLoad:
    """Test cases for the maximize_load function."""
    
    def test_perfect_fit_scenario(self):
        """Test case where items fit perfectly with no leftover space."""
        container_dim = (60.0, 40.0, 30.0)
        item_dim = (20.0, 20.0, 15.0)
        
        result = maximize_load(container_dim, item_dim, item_volume_margin=1.0)
        
        assert result["max_count"] == 12
        assert result["leftover_percentage"] == 0.0
    
    def test_acceptable_surplus_5_percent(self):
        """Test case with approximately 5% leftover space (acceptable)."""
        container_dim = (20.0, 10.0, 10.0)
        item_dim = (9.8, 4.8, 4.8)
        
        result = maximize_load(container_dim, item_dim, item_volume_margin=0.95)
        
        assert result["max_count"] == 8
        assert result["leftover_percentage"] < 10.0
        assert result["leftover_percentage"] > 5.0  # Should be around 9.68%
    
    def test_five_percent_leftover_case(self):
        """Test case designed to have approximately 5% leftover."""
        container_dim = (20.5, 20.5, 10.0)
        item_dim = (10.0, 10.0, 4.8)
        
        result = maximize_load(container_dim, item_dim, item_volume_margin=0.95)
        
        assert result["max_count"] == 8
        assert result["leftover_percentage"] < 10.0
        assert result["leftover_percentage"] > 5.0  # Should be around 8.63%
    
    def test_inefficient_packing_exception(self):
        """Test case where leftover space exceeds 10% and should raise exception."""
        container_dim = (100.0, 100.0, 100.0)
        item_dim = (30.0, 30.0, 30.0)
        
        with pytest.raises(ValueError, match="Inefficient packing.*exceeds 10% limit"):
            maximize_load(container_dim, item_dim, item_volume_margin=0.95)
    
    def test_item_larger_than_container(self):
        """Test case where item dimensions exceed container dimensions."""
        container_dim = (10.0, 10.0, 10.0)
        item_dim = (15.0, 5.0, 5.0)  # Length exceeds container
        
        with pytest.raises(ValueError, match="Item dimensions exceed container dimensions"):
            maximize_load(container_dim, item_dim)
    
    def test_invalid_volume_margin(self):
        """Test case with invalid volume margin values."""
        container_dim = (20.0, 20.0, 20.0)
        item_dim = (10.0, 10.0, 10.0)
        
        with pytest.raises(ValueError, match="item_volume_margin must be between 0 and 1"):
            maximize_load(container_dim, item_dim, item_volume_margin=-0.1)
        
        with pytest.raises(ValueError, match="item_volume_margin must be between 0 and 1"):
            maximize_load(container_dim, item_dim, item_volume_margin=1.1)
        
        with pytest.raises(ValueError, match="item_volume_margin must be between 0 and 1"):
            maximize_load(container_dim, item_dim, item_volume_margin=0.0)
    
    def test_volume_constraint_limits_packing(self):
        """Test case where volume constraint is more restrictive than geometric constraint."""
        container_dim = (30.0, 30.0, 30.0)
        item_dim = (10.0, 10.0, 10.0)
        
        with pytest.raises(ValueError, match="Inefficient packing.*exceeds 10% limit"):
            maximize_load(container_dim, item_dim, item_volume_margin=0.5)
    
    def test_edge_case_single_item(self):
        """Test case where only one item fits."""
        container_dim = (10.3, 10.3, 10.3)
        item_dim = (10.0, 10.0, 10.0)
        
        result = maximize_load(container_dim, item_dim, item_volume_margin=0.95)
        
        assert result["max_count"] == 1
        assert result["leftover_percentage"] < 10.0
        assert result["leftover_percentage"] > 0.0  # Should be around 8.49%
    
    def test_volume_margin_constraint(self):
        """Test case where volume margin limits the number of items."""
        container_dim = (20.0, 20.0, 20.0)
        item_dim = (9.0, 9.0, 9.0)
        
        with pytest.raises(ValueError, match="Inefficient packing.*exceeds 10% limit"):
            maximize_load(container_dim, item_dim, item_volume_margin=0.8)
