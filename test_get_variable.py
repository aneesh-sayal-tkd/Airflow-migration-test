#!/usr/bin/env python3
"""
Test file for the simple get_variable function
Run this from the project root directory
"""

import sys
import os
import json

# Add src to path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from utils import CommonUtils, CommonUtilsConstants
from airflow import AirflowUtilsConstants

# ===== CONFIGURATION =====
# Specify your MWAA environment name here
MWAA_ENVIRONMENT_NAME = "MWAA1USVGA10883D1006"  # Your actual environment name

def get_variable(environment, region, airflow_environment_name):
    """
    Simple function to get variables from MWAA environment
    Returns the raw response for debugging
    """
    try:
        mwaa_client = CommonUtils.get_boto3_client(AirflowUtilsConstants.MWAA_KEY, environment, region)

        request_params = {
            "Name": airflow_environment_name,
            "Path": "/variables",
            "Method": "GET",
        }
        
        print(f"Making API call with params: {request_params}")
        response = mwaa_client.invoke_rest_api(**request_params)
        
        print(f"Response keys: {list(response.keys()) if response else 'No response'}")
        print(f"Response metadata: {response.get('ResponseMetadata', {})}")
        
        # Check if we have a response body
        if response.get('ResponseBody'):
            try:
                content = response['ResponseBody'].read().decode('utf-8')
                print(f"Response body content: '{content}'")
                print(f"Content length: {len(content)}")
                print("Airflow REST API successful, variable retrieved")
                return response, content
            except Exception as read_error:
                print(f"Error reading response body: {read_error}")
                return response, None
        else:
            print("No ResponseBody in response")
            return response, None
            
    except Exception as ex:
        status_message = f"Unable to get variable from airflow env: {str(ex)}"
        print(status_message)
        raise Exception(status_message)

def test_basic_setup():
    """Test basic configuration setup"""
    print("=== Testing Basic Setup ===")
    try:
        env = CommonUtils.get_current_environment()
        region = CommonUtils.get_current_region()
        
        print(f"✅ Environment: {env}")
        print(f"✅ Region: {region}")
        
        return True, env, region
    except Exception as e:
        print(f"❌ Basic setup failed: {e}")
        return False, None, None

def test_mwaa_client():
    """Test MWAA client creation"""
    print("\n=== Testing MWAA Client Creation ===")
    try:
        env = CommonUtils.get_current_environment()
        region = CommonUtils.get_current_region()
        
        mwaa_client = CommonUtils.get_boto3_client("mwaa", env, region)
        print("✅ MWAA client created successfully")
        
        # Test if environment exists
        response = mwaa_client.list_environments()
        environments = response.get('Environments', [])
        print(f"✅ Found {len(environments)} MWAA environments")
        
        if MWAA_ENVIRONMENT_NAME in environments:
            print(f"✅ Target environment '{MWAA_ENVIRONMENT_NAME}' found")
            return True
        else:
            print(f"⚠️  Target environment '{MWAA_ENVIRONMENT_NAME}' not found")
            print(f"Available environments: {environments}")
            return False
            
    except Exception as e:
        print(f"❌ MWAA client creation failed: {e}")
        return False

def test_get_variable_function():
    """Test the get_variable function"""
    print(f"\n=== Testing get_variable Function ===")
    print(f"Target Environment: {MWAA_ENVIRONMENT_NAME}")
    
    try:
        env = CommonUtils.get_current_environment()
        region = CommonUtils.get_current_region()
        
        print(f"Calling get_variable with:")
        print(f"  Environment: {env}")
        print(f"  Region: {region}")
        print(f"  MWAA Environment: {MWAA_ENVIRONMENT_NAME}")
        print("-" * 50)
        
        # Call the function
        response, content = get_variable(env, region, MWAA_ENVIRONMENT_NAME)
        
        print("-" * 50)
        print("=== ANALYSIS OF RESPONSE ===")
        
        # Analyze the response
        if response:
            print("✅ Function executed without exceptions")
            
            # Check HTTP status
            http_status = response.get('ResponseMetadata', {}).get('HTTPStatusCode', 'Unknown')
            print(f"HTTP Status Code: {http_status}")
            
            if http_status == 200:
                print("✅ HTTP 200 - API call was successful")
            else:
                print(f"⚠️  HTTP {http_status} - API call may have issues")
            
            # Analyze content
            if content is not None:
                if content.strip():
                    print(f"✅ Response has content ({len(content)} characters)")
                    
                    # Try to parse as JSON
                    try:
                        json_data = json.loads(content)
                        print("✅ Content is valid JSON")
                        print(f"JSON structure: {type(json_data)}")
                        
                        if isinstance(json_data, dict):
                            print(f"JSON keys: {list(json_data.keys())}")
                            
                            # Look for variables
                            if 'variables' in json_data:
                                variables = json_data['variables']
                                print(f"✅ Found 'variables' key with {len(variables)} items")
                                
                                if variables:
                                    print("Sample variables:")
                                    for i, var in enumerate(variables[:3], 1):
                                        if isinstance(var, dict):
                                            key = var.get('key', 'Unknown')
                                            value = str(var.get('value', 'Unknown'))[:50]
                                            print(f"  {i}. {key}: {value}")
                                        else:
                                            print(f"  {i}. {var}")
                                else:
                                    print("Variables list is empty")
                            else:
                                print("No 'variables' key found in JSON")
                                print("Available keys:", list(json_data.keys()))
                        
                        elif isinstance(json_data, list):
                            print(f"JSON is a list with {len(json_data)} items")
                        
                        return True
                        
                    except json.JSONDecodeError:
                        print("⚠️  Content is not valid JSON")
                        print("Content preview:", content[:200])
                        
                        # Check if it might be HTML or other format
                        if content.lower().startswith('<!doctype') or content.lower().startswith('<html'):
                            print("Content appears to be HTML - might be an error page")
                        
                        return True  # Still a valid response, just not JSON
                
                else:
                    print("✅ API call successful but returned empty content")
                    print("💡 This usually means no variables are configured in the environment")
                    return True
            else:
                print("❌ Could not read response content")
                return False
        else:
            print("❌ No response received")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        print("Full traceback:")
        traceback.print_exc()
        return False

def main():
    """Main test execution"""
    print("🚀 Testing get_variable Function")
    print(f"Target MWAA Environment: {MWAA_ENVIRONMENT_NAME}")
    print("=" * 60)
    
    # Test 1: Basic Setup
    success, env, region = test_basic_setup()
    if not success:
        print("❌ Cannot continue - basic setup failed")
        return
    
    # Test 2: MWAA Client
    client_success = test_mwaa_client()
    if not client_success:
        print("⚠️  MWAA client issues, but continuing with function test...")
    
    # Test 3: get_variable Function
    function_success = test_get_variable_function()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    tests = [
        ("Basic Setup", success),
        ("MWAA Client", client_success),
        ("get_variable Function", function_success)
    ]
    
    for test_name, result in tests:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    if function_success:
        print("\n🎉 get_variable function is working!")
        print("You can now analyze the response format to build your full function.")
    else:
        print("\n⚠️  get_variable function needs debugging.")
        print("Check the error messages above for details.")

if __name__ == "__main__":
    if MWAA_ENVIRONMENT_NAME == "MWAA1USVGA10883D1006":
        print("⚠️  Please update MWAA_ENVIRONMENT_NAME with your actual environment name")
        print("Edit the variable at the top of this file before running")
    
    main()
