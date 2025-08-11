#!/usr/bin/env python3
"""
Test file for CommonUtils functions
Run this from the project root directory
"""

import sys
import os

# Add src to path so we can import our utils
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from utils.CommonUtils import (
    get_config,
    client_auth,
    read_secret,
    get_boto3_client,
    get_current_environment,
    get_current_region,
    get_aws_region
)

def test_config():
    """Test configuration loading"""
    print("=== Testing Configuration ===")
    try:
        config = get_config()
        print("✅ Config loaded successfully")
        print(f"Environment: {config.get('environment', 'Not found')}")
        print(f"Region: {config.get('region', 'Not found')}")
        return True
    except Exception as e:
        print(f"❌ Config loading failed: {e}")
        return False

def test_vault_auth():
    """Test Vault authentication"""
    print("\n=== Testing Vault Authentication ===")
    try:
        client = client_auth()
        if client:
            print("✅ Vault authentication successful")
            print(f"Vault URL: {client.url}")
            return True
        else:
            print("❌ Vault authentication failed")
            return False
    except Exception as e:
        print(f"❌ Vault authentication error: {e}")
        return False

def test_environment_functions():
    """Test environment and region functions"""
    print("\n=== Testing Environment Functions ===")
    try:
        env = get_current_environment()
        region = get_current_region()
        aws_region = get_aws_region(region)
        
        print(f"✅ Current Environment: {env}")
        print(f"✅ Current Region: {region}")
        print(f"✅ AWS Region: {aws_region}")
        return True
    except Exception as e:
        print(f"❌ Environment functions error: {e}")
        return False

def test_mwaa_configurations():
    """Test to list all MWAA configurations in AWS"""
    print("\n=== Testing MWAA Configurations ===")
    try:
        env = get_current_environment()
        region = get_current_region()
        
        # Create MWAA client
        mwaa_client = get_boto3_client('mwaa', env, region)
        
        # List all MWAA environments
        response = mwaa_client.list_environments()
        envs = response.get('Environments', [])
        print(f"✅ Found {len(envs)} MWAA environments")
        
        if len(envs) == 0:
            print("No MWAA environments found in this region")
            return True
        
        # Get detailed configuration for each environment
        for env_name in envs:
            print(f"\n--- MWAA Environment: {env_name} ---")
            try:
                env_detail = mwaa_client.get_environment(Name=env_name)
                environment_info = env_detail.get('Environment', {})
                
                # Display key configuration details
                key_configs = [
                    'Name', 'Status', 'AirflowVersion', 'ExecutionRoleArn',
                    'DagS3Path']
                
                for key in key_configs:
                    if key in environment_info:
                        print(f"  {key}: {environment_info[key]}")
                        
            except Exception as detail_error:
                print(f"  ❌ Error getting details for {env_name}: {detail_error}")
            
            print("-" * 40)
        
        return True
    except Exception as e:
        print(f"❌ MWAA configurations error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting CommonUtils Testing...\n")
    
    tests = [
        test_config,
        test_environment_functions,
        test_vault_auth,
        test_mwaa_configurations,  # New MWAA test
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print("-" * 50)
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check your configuration and credentials.")

if __name__ == "__main__":
    main()
