#!/usr/bin/env python3
"""
Seed script to populate the database with sample item catalog data.

This script creates sample SKUs with different dimensions for testing
the container loading optimization algorithm.
"""

from sqlmodel import Session
from database import engine, create_db_and_tables
from models import ItemCatalog


def seed_data():
    """Insert sample data into the ItemCatalog table."""
    
    create_db_and_tables()
    
    sample_items = [
        ItemCatalog(
            sku="SKU001",
            name="Standard Box A",
            length=30.0,
            width=20.0,
            height=15.0,
            weight=2.5
        ),
        ItemCatalog(
            sku="SKU002", 
            name="Large Box B",
            length=50.0,
            width=40.0,
            height=30.0,
            weight=8.0
        ),
        ItemCatalog(
            sku="SKU003",
            name="Small Box C", 
            length=15.0,
            width=10.0,
            height=8.0,
            weight=0.8
        )
    ]
    
    with Session(engine) as session:
        existing_count = len(session.query(ItemCatalog).all())
        
        if existing_count > 0:
            print(f"Database already contains {existing_count} items. Skipping seed.")
            return
        
        for item in sample_items:
            session.add(item)
        
        session.commit()
        print(f"Successfully seeded {len(sample_items)} items to the database.")
        
        print("\nSeeded items:")
        for item in sample_items:
            print(f"- {item.sku}: {item.name} ({item.length}x{item.width}x{item.height}cm, {item.weight}kg)")


if __name__ == "__main__":
    seed_data()
