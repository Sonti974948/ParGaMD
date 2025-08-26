#!/usr/bin/env python3
"""
Test script for ParGaMD Reweighting Tool
========================================

This script tests the tool with the provided example data files.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_test(command, description):
    """Run a test command and report results."""
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"Command: {command}")
    print('='*60)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ SUCCESS")
            if result.stdout:
                print("Output:")
                print(result.stdout)
        else:
            print("❌ FAILED")
            print("Error:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False
    
    return True

def main():
    """Run all tests."""
    print("ParGaMD Reweighting Tool - Test Suite")
    print("="*60)
    
    # Check if required files exist
    required_files = [
        'pargamd_reweighting.py',
        'example_data_1d.dat',
        'example_data_2d.dat',
        'config_ce_1d.yaml',
        'config_ce_2d.yaml',
        'config_mc_2d.yaml'
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    print("✅ All required files found")
    
    # Test 1: CE 1D with command line arguments
    test1 = run_test(
        "python pargamd_reweighting.py ce --input example_data_1d.dat --dimensions 1d --temperature 300 --output-dir test_results_ce_1d",
        "CE 1D reweighting with command line arguments"
    )
    
    # Test 2: CE 2D with command line arguments
    test2 = run_test(
        "python pargamd_reweighting.py ce --input example_data_2d.dat --dimensions 2d --temperature 300 --output-dir test_results_ce_2d",
        "CE 2D reweighting with command line arguments"
    )
    
    # Test 3: MC 2D with command line arguments
    test3 = run_test(
        "python pargamd_reweighting.py mc --input example_data_2d.dat --order 5 --temperature 300 --output-dir test_results_mc_2d",
        "MC 2D reweighting with command line arguments"
    )
    
    # Test 4: CE 1D with config file
    test4 = run_test(
        "python pargamd_reweighting.py ce --config config_ce_1d.yaml --input example_data_1d.dat",
        "CE 1D reweighting with config file"
    )
    
    # Test 5: CE 2D with config file
    test5 = run_test(
        "python pargamd_reweighting.py ce --config config_ce_2d.yaml --input example_data_2d.dat",
        "CE 2D reweighting with config file"
    )
    
    # Test 6: MC 2D with config file
    test6 = run_test(
        "python pargamd_reweighting.py mc --config config_mc_2d.yaml --input example_data_2d.dat",
        "MC 2D reweighting with config file"
    )
    
    # Test 7: With plotting
    test7 = run_test(
        "python pargamd_reweighting.py ce --input example_data_2d.dat --dimensions 2d --temperature 300 --plot --output-dir test_results_with_plots",
        "CE 2D reweighting with plotting"
    )
    
    # Test 8: Help commands
    test8 = run_test(
        "python pargamd_reweighting.py --help",
        "Main help command"
    )
    
    test9 = run_test(
        "python pargamd_reweighting.py ce --help",
        "CE method help command"
    )
    
    test10 = run_test(
        "python pargamd_reweighting.py mc --help",
        "MC method help command"
    )
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)
    
    tests = [test1, test2, test3, test4, test5, test6, test7, test8, test9, test10]
    passed = sum(tests)
    total = len(tests)
    
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("\nThe ParGaMD Reweighting Tool is working correctly.")
        print("You can now use it with your own data files.")
        return True
    else:
        print("❌ SOME TESTS FAILED")
        print("Please check the error messages above and fix any issues.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

