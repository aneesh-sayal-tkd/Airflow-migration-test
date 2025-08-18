#!/usr/bin/env python3
"""
Focused MWAA test - create variable in specified environment
Run this from the project root directory
"""

import sys
import os

# Add src to path so we can import modules
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
from utils import CommonUtilsConstants
from airflow.AirflowUtils import create_variable


# ---- Configuration ----
MWAA_ENVIRONMENT_NAME = "MWAA1USVGA10612D1023"  # Put your MWAA environment name here


def test_prerequisites():
    print("=== Testing prerequisites: Config and Vault authentication ===")
    try:
        config = get_config()
        print("✅ Config loaded.")
        client = client_auth()
        if client:
            print("✅ Vault authentication successful.")
            return True
        else:
            print("❌ Vault authentication failed.")
            return False
    except Exception as e:
        print(f"❌ Prerequisite test failed: {e}")
        return False


def test_create_variable():
    print(f"\n=== Testing creating variable in MWAA environment: {MWAA_ENVIRONMENT_NAME} ===")
    try:
        env = get_current_environment()
        region = get_current_region()

        result = create_variable(
            key="test_key",
            value="test_value",
            environment=env,
            region=region,
            airflow_environment_name=MWAA_ENVIRONMENT_NAME
        )

        print(f"Result: {result}")

        if result.get("status") == CommonUtilsConstants.SUCCESS_KEY:
            print("✅ Variable created successfully.")
            return True
        else:
            print(f"❌ Failed to create variable: {result.get('error')}")
            return False
    except Exception as e:
        print(f"❌ Exception during create variable test: {e}")
        return False


def main():
    if MWAA_ENVIRONMENT_NAME == "your_actual_mwaa_environment":
        print("Please update MWAA_ENVIRONMENT_NAME with your real MWAA environment name.")
        return

    if not test_prerequisites():
        print("Prerequisites failed. Cannot continue.")
        return

    if not test_create_variable():
        print("Create variable test failed.")
    else:
        print("All tests passed successfully.")


if __name__ == "__main__":
    main()
