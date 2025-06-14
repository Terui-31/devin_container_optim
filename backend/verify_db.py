#!/usr/bin/env python3
"""
Verification script to check database schema and data.
"""

from sqlmodel import Session, select
from database import engine
from models import ItemCatalog
import os

def verify_database():
    """Verify database schema and data."""
    
    db_file = "app.db"
    if os.path.exists(db_file):
        print(f"✅ Database file '{db_file}' exists")
    else:
        print(f"❌ Database file '{db_file}' not found")
        return False
    
    try:
        with Session(engine) as session:
            items = session.exec(select(ItemCatalog)).all()
            print(f"✅ Found {len(items)} items in ItemCatalog table")
            
            if len(items) != 3:
                print(f"❌ Expected 3 items, found {len(items)}")
                return False
            
            for item in items:
                print(f"  📦 {item.sku}: {item.name}")
                print(f"     Dimensions: {item.length}x{item.width}x{item.height}cm")
                print(f"     Weight: {item.weight}kg")
                
                if not item.sku or not item.name:
                    print(f"❌ Missing required string field")
                    return False
                
                if item.length <= 0 or item.width <= 0 or item.height <= 0 or item.weight <= 0:
                    print(f"❌ Invalid numeric values")
                    return False
            
            print("✅ All items have valid data")
            return True
            
    except Exception as e:
        print(f"❌ Database verification failed: {e}")
        return False

if __name__ == "__main__":
    success = verify_database()
    if success:
        print("\n🎉 Database schema and data verification successful!")
    else:
        print("\n💥 Database verification failed!")
        exit(1)
