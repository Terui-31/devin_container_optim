#!/usr/bin/env python3
"""
Basic test script to verify core API functionality without complex imports.
"""

import sys
import os

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'backend'))

def test_optimizer_basic():
    """Test that the optimizer function works correctly."""
    try:
        from backend.optimizer import maximize_load
        
        result = maximize_load((60, 40, 30), (30, 20, 15), 1.0)
        assert result["max_count"] == 8
        assert result["leftover_percentage"] == 0.0
        print("✓ Optimizer basic test passed")
        return True
    except Exception as e:
        print(f"✗ Optimizer test failed: {e}")
        return False

def test_fastapi_imports():
    """Test that FastAPI components can be imported."""
    try:
        from fastapi.testclient import TestClient
        from fastapi import FastAPI
        print("✓ FastAPI imports successful")
        return True
    except Exception as e:
        print(f"✗ FastAPI import failed: {e}")
        return False

def test_sqlmodel_basic():
    """Test basic SQLModel functionality."""
    try:
        from sqlmodel import SQLModel, create_engine, Session
        from sqlmodel.pool import StaticPool
        
        engine = create_engine("sqlite://", poolclass=StaticPool)
        print("✓ SQLModel basic test passed")
        return True
    except Exception as e:
        print(f"✗ SQLModel test failed: {e}")
        return False

if __name__ == "__main__":
    print("Running basic functionality tests...")
    
    tests = [
        test_optimizer_basic,
        test_fastapi_imports,
        test_sqlmodel_basic
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All basic tests passed - core functionality works")
        sys.exit(0)
    else:
        print("✗ Some tests failed")
        sys.exit(1)
