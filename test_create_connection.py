#!/usr/bin/env python3
"""
Simple test for create_connection function in MWAA.
Run from project root.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from airflow.AirflowUtils import create_connection
from utils import CommonUtils, CommonUtilsConstants

# Replace with your actual MWAA environment name before running
MWAA_ENVIRONMENT_NAME = ""

def test_prerequisites():
    try:
        config = CommonUtils.get_config()
        print("✅ Config loaded OK.")
        vault_client = CommonUtils.client_auth()
        if vault_client:
            print("✅ Vault authentication successful.")
            return True
        else:
            print("❌ Vault authentication failed.")
            return False
    except Exception as e:
        print(f"❌ Error during prerequisites: {e}")
        return False

def test_create_connection():
    print("\n=== Testing create_connection ===")
    try:
        environment = CommonUtils.get_current_environment()
        region = CommonUtils.get_current_region()

        result = create_connection(
            connection_id="test_conn_01",
            conn_type="databricks",
            description="Test Postgres connection",
            host="db.example.com",
            login="user",
            password="password",
            schema="public",
            port=5432,
            extra="",
            environment=environment,
            region=region,
            airflow_environment_name=MWAA_ENVIRONMENT_NAME
        )

        print(f"Result: {result}")

        if result.get("status") == CommonUtilsConstants.SUCCESS_KEY:
            return True
        else:
            return False
    except Exception as e:
        print(f"❌ Exception during create_connection test: {e}")
        return False

def main():
    if MWAA_ENVIRONMENT_NAME == "your_actual_mwaa_environment":
        print("Please update MWAA_ENVIRONMENT_NAME with your real MWAA environment name.")
        return

    if not test_prerequisites():
        print("Prerequisites failed. Exiting.")
        return

    if not test_create_connection():
        print("Create connection test failed.")
    else:
        print("Create connection test succeeded.")

if __name__ == "__main__":
    main()
