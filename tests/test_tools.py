#!/usr/bin/env python3
"""
Test script to verify GDB extension works correctly
"""

import subprocess
import sys
import os
from pathlib import Path

def test_gdb_extension():
    """Test that the GDB extension loads correctly"""
    
    # Get repository root
    repo_root = Path(__file__).parent.parent
    gdb_script = repo_root / "scripts" / "gdb_acd.py"
    
    if not gdb_script.exists():
        print(f"Error: GDB script not found at {gdb_script}")
        return False
    
    # Test that the script is syntactically valid Python
    try:
        with open(gdb_script, 'r') as f:
            code = f.read()
        
        # Try to compile the script (syntax check only)
        compile(code, str(gdb_script), 'exec')
        
        print("✓ GDB extension syntax is valid")
        print("  (Note: Full GDB testing requires running within GDB)")
        return True
        
    except SyntaxError as e:
        print(f"✗ GDB extension has syntax error: {e}")
        return False
    except Exception as e:
        print(f"✗ GDB extension test failed: {e}")
        return False


def test_parser():
    """Test that the parser works correctly"""
    
    repo_root = Path(__file__).parent.parent
    parser_script = repo_root / "src" / "acd_parser.py"
    examples_dir = repo_root / "examples"
    
    if not parser_script.exists():
        print(f"Error: Parser script not found at {parser_script}")
        return False
    
    # Test running the parser
    try:
        result = subprocess.run(
            [sys.executable, str(parser_script), str(examples_dir), "--analyze"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print(f"Error running parser: {result.stderr}")
            return False
        
        # Check for expected output
        if "Implementation Status Analysis" in result.stdout:
            print("✓ Parser analysis works correctly")
            return True
        else:
            print("✗ Parser output missing expected content")
            return False
        
    except subprocess.TimeoutExpired:
        print("✗ Parser test timed out")
        return False
    except Exception as e:
        print(f"✗ Parser test failed: {e}")
        return False


def test_validator():
    """Test that the validator works correctly"""
    
    repo_root = Path(__file__).parent.parent
    validator_script = repo_root / "src" / "validate_acd.py"
    examples_dir = repo_root / "examples"
    
    if not validator_script.exists():
        print(f"Error: Validator script not found at {validator_script}")
        return False
    
    # Test running the validator
    try:
        result = subprocess.run(
            [sys.executable, str(validator_script), str(examples_dir)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print(f"Error running validator: {result.stderr}")
            return False
        
        # Check for expected output
        if "ACD Validation Report" in result.stdout:
            print("✓ Validator works correctly")
            return True
        else:
            print("✗ Validator output missing expected content")
            return False
        
    except subprocess.TimeoutExpired:
        print("✗ Validator test timed out")
        return False
    except Exception as e:
        print(f"✗ Validator test failed: {e}")
        return False


def test_header_example():
    """Test that header example compiles"""
    
    repo_root = Path(__file__).parent.parent
    header_example = repo_root / "examples" / "header_example.cpp"
    
    if not header_example.exists():
        print(f"Error: Header example not found at {header_example}")
        return False
    
    # Test compiling
    try:
        result = subprocess.run(
            ["g++", "-o", "/tmp/test_header_example", str(header_example), "-std=c++11"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print(f"Error compiling header example: {result.stderr}")
            return False
        
        print("✓ Header example compiles successfully")
        return True
        
    except subprocess.TimeoutExpired:
        print("✗ Compilation test timed out")
        return False
    except FileNotFoundError:
        print("⚠ g++ not found - skipping compilation test")
        return True  # Don't fail if g++ is not available
    except Exception as e:
        print(f"✗ Compilation test failed: {e}")
        return False


def main():
    print("=" * 70)
    print("ACD Tools Test Suite")
    print("=" * 70)
    print()
    
    tests = [
        ("GDB Extension", test_gdb_extension),
        ("ACD Parser", test_parser),
        ("ACD Validator", test_validator),
        ("Header Example", test_header_example),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        print(f"Testing {name}...")
        if test_func():
            passed += 1
        else:
            failed += 1
        print()
    
    print("=" * 70)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 70)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
