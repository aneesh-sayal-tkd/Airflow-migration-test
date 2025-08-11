#!/usr/bin/env python3
"""
Focused MWAA test file for specific environment testing
Tests: boto3 MWAA connection, variables, and connections for a specified environment
Run this from the project root directory
"""

import sys
import os

# Add src to path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from utils import (
    get_config,
    get_boto3_client,
    get_current_environment,
    get_current_region,
    CommonUtilsConstants
)

from airflow.AirflowUtils import (
    get_environment_variables,
    get_environment_connections
)

# ===== CONFIGURATION =====
# Specify your MWAA environment name here
MWAA_ENVIRONMENT_NAME = "MWAA1USVGA10612D1023"  # Replace with your actual environment name

def test_basic_setup():
    """Test basic configuration and environment setup"""
    print("=== Testing Basic Setup ===")
    try:
        config = get_config()
        env = get_current_environment()
        region = get_current_region()
        
        print(f"✅ Config loaded successfully")
        print(f"✅ Environment: {env}")
        print(f"✅ Region: {region}")
        
        return True, env, region
    except Exception as e:
        print(f"❌ Basic setup failed: {e}")
        return False, None, None

def test_mwaa_client_connection(environment, region):
    """Test MWAA client creation"""
    print("\n=== Testing MWAA Client Connection ===")
    try:
        # Create MWAA client using your CommonUtils function
        mwaa_client = get_boto3_client("mwaa", environment, region)
        print("✅ MWAA client created successfully")
        
        # Test basic MWAA operation - list environments to verify connection
        response = mwaa_client.list_environments()
        environments = response.get('Environments', [])
        
        print(f"✅ MWAA connection verified - found {len(environments)} environments")
        
        # Check if our target environment exists
        if MWAA_ENVIRONMENT_NAME in environments:
            print(f"✅ Target environment '{MWAA_ENVIRONMENT_NAME}' found")
            return True, mwaa_client
        else:
            print(f"⚠️  Target environment '{MWAA_ENVIRONMENT_NAME}' not found")
            print(f"Available environments: {environments}")
            return False, mwaa_client
            
    except Exception as e:
        print(f"❌ MWAA client connection failed: {e}")
        return False, None

def get_variable(environment, region):
    """Test getting variables from the specified MWAA environment"""
    print(f"\n=== Testing Variables from '{MWAA_ENVIRONMENT_NAME}' ===")
    try:
        result = get_environment_variables(environment, region, MWAA_ENVIRONMENT_NAME)
        
        if result[CommonUtilsConstants.STATUS_KEY] == CommonUtilsConstants.SUCCESS_KEY:
            variables = result[CommonUtilsConstants.RESULT_KEY]['variables']
            count = result[CommonUtilsConstants.RESULT_KEY]['variables_count']
            
            print(f"✅ Successfully retrieved {count} variables")
            
            if variables:
                print("\n--- Variables Found ---")
                for i, var in enumerate(variables, 1):
                    key = var.get('key', 'Unknown')
                    value = str(var.get('value', 'Unknown'))
                    # Truncate long values for display
                    display_value = value[:100] + '...' if len(value) > 100 else value
                    print(f"{i:2d}. {key}: {display_value}")
                    
                    # Show only first 10 for readability
                    if i >= 10:
                        print(f"    ... and {count - 10} more variables")
                        break
            else:
                print("No variables found in this environment")
                
            return True
        else:
            print(f"❌ Failed to get variables: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Variables retrieval error: {e}")
        return False

def test_get_connections(environment, region):
    """Test getting connections from the specified MWAA environment"""
    print(f"\n=== Testing Connections from '{MWAA_ENVIRONMENT_NAME}' ===")
    try:
        result = get_environment_connections(environment, region, MWAA_ENVIRONMENT_NAME)
        
        if result[CommonUtilsConstants.STATUS_KEY] == CommonUtilsConstants.SUCCESS_KEY:
            connections = result[CommonUtilsConstants.RESULT_KEY]['connections']
            count = result[CommonUtilsConstants.RESULT_KEY]['connections_count']
            
            print(f"✅ Successfully retrieved {count} connections")
            
            if connections:
                print("\n--- Connections Found ---")
                for i, conn in enumerate(connections, 1):
                    conn_id = conn.get('conn_id', 'Unknown')
                    conn_type = conn.get('conn_type', 'Unknown')
                    host = conn.get('host', 'No host')
                    description = conn.get('description', 'No description')
                    
                    print(f"{i:2d}. {conn_id}")
                    print(f"    Type: {conn_type}")
                    print(f"    Host: {host}")
                    print(f"    Description: {description}")
                    print()
                    
                    # Show only first 5 for readability
                    if i >= 5:
                        print(f"    ... and {count - 5} more connections")
                        break
            else:
                print("No connections found in this environment")
                
            return True
        else:
            print(f"❌ Failed to get connections: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Connections retrieval error: {e}")
        return False

def main():
    """Main test execution"""
    print("🚀 MWAA Specific Environment Testing")
    print(f"Target Environment: {MWAA_ENVIRONMENT_NAME}")
    print("=" * 60)
    
    # Test 1: Basic Setup
    success, env, region = test_basic_setup()
    if not success:
        print("❌ Cannot continue - basic setup failed")
        return
    
    # Test 2: MWAA Client Connection
    success, mwaa_client = test_mwaa_client_connection(env, region)
    if not success:
        print("❌ Cannot continue - MWAA client connection failed")
        return
    
    # Test 3: Get Variables
    variables_success = test_get_variables(env, region)
    
    # Test 4: Get Connections
    connections_success = test_get_connections(env, region)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    tests = [
        ("Basic Setup", True),
        ("MWAA Client Connection", True),
        ("Variables Retrieval", variables_success),
        ("Connections Retrieval", connections_success)
    ]
    
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for test_name, result in tests:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your MWAA setup is working perfectly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    print("Please update MWAA_ENVIRONMENT_NAME variable with your actual environment name!")
    print(f"Current value: {MWAA_ENVIRONMENT_NAME}")
    
    if MWAA_ENVIRONMENT_NAME == "your-mwaa-environment-name":
        print("\n⚠️  Please edit the MWAA_ENVIRONMENT_NAME variable at the top of this file")
        print("Set it to your actual MWAA environment name before running the test.")
        sys.exit(1)
    
    main()
