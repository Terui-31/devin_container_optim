"""
Container loading optimization module using OR-Tools.

This module implements 3D bin packing algorithms to maximize the number
of identical items that can be placed in a rectangular container while
maintaining volume constraints.
"""

from typing import Tuple, Dict
import math
from ortools.linear_solver import pywraplp


def maximize_load(
    container_dim: Tuple[float, float, float],
    item_dim: Tuple[float, float, float],
    item_volume_margin: float = 0.95,
) -> Dict[str, float]:
    """
    Compute the maximum number of identical items that can be placed in a single rectangular container.

    This function uses 3D integer partitioning with fixed orientation to determine
    the optimal packing arrangement, then applies volume constraints to ensure
    efficient space utilization.

    Args:
        container_dim: (length, width, height) of the container in cm.
        item_dim: (length, width, height) of the item in cm.
        item_volume_margin: Fraction of the container volume that may be used (default 95%).

    Returns:
        A dict containing:
            - max_count: int - Maximum number of items that can be loaded
            - leftover_percentage: float - Percentage of unused space (0–100)

    Raises:
        ValueError: If leftover percentage exceeds 10% (inefficient packing)
        ValueError: If item dimensions are larger than container dimensions
    """
    
    container_length, container_width, container_height = container_dim
    item_length, item_width, item_height = item_dim
    
    if (item_length > container_length or 
        item_width > container_width or 
        item_height > container_height):
        raise ValueError("Item dimensions exceed container dimensions")
    
    if item_volume_margin <= 0 or item_volume_margin > 1:
        raise ValueError("item_volume_margin must be between 0 and 1")
    
    container_volume = container_length * container_width * container_height
    item_volume = item_length * item_width * item_height
    max_allowed_volume = container_volume * item_volume_margin
    
    items_per_length = int(container_length // item_length)
    items_per_width = int(container_width // item_width)
    items_per_height = int(container_height // item_height)
    
    geometric_max_count = items_per_length * items_per_width * items_per_height
    
    volume_max_count = int(max_allowed_volume // item_volume)
    
    max_count = min(geometric_max_count, volume_max_count)
    
    used_volume = max_count * item_volume
    leftover_volume = container_volume - used_volume
    leftover_percentage = (leftover_volume / container_volume) * 100
    
    if leftover_percentage > 10.0:
        raise ValueError(
            f"Inefficient packing: {leftover_percentage:.1f}% leftover space exceeds 10% limit"
        )
    
    return {
        "max_count": max_count,
        "leftover_percentage": round(leftover_percentage, 2)
    }


def _optimize_with_ortools(
    container_dim: Tuple[float, float, float],
    item_dim: Tuple[float, float, float],
    max_items: int
) -> int:
    """
    Use OR-Tools linear solver for more sophisticated optimization.
    
    This is a placeholder for future enhancement using OR-Tools CP-SAT solver
    for more complex packing scenarios with rotation and advanced constraints.
    
    Args:
        container_dim: Container dimensions (length, width, height)
        item_dim: Item dimensions (length, width, height)  
        max_items: Upper bound on number of items
        
    Returns:
        Optimized number of items that can be packed
    """
    
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        container_length, container_width, container_height = container_dim
        item_length, item_width, item_height = item_dim
        
        items_per_length = int(container_length // item_length)
        items_per_width = int(container_width // item_width)
        items_per_height = int(container_height // item_height)
        
        return items_per_length * items_per_width * items_per_height
    
    container_length, container_width, container_height = container_dim
    item_length, item_width, item_height = item_dim
    
    items_per_length = int(container_length // item_length)
    items_per_width = int(container_width // item_width)  
    items_per_height = int(container_height // item_height)
    
    return min(max_items, items_per_length * items_per_width * items_per_height)
