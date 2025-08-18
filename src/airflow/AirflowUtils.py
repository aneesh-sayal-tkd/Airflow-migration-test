#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = "ZS Associates"

"""
AirflowUtils.py - AWS MWAA (Managed Workflows for Apache Airflow) Utilities
Tech Description: This utility provides functions for managing AWS MWAA environments
Pre_requisites: Requires AirflowUtilsConstants.py and CommonUtils.py
"""

import traceback
import json
from botocore.exceptions import ClientError
from typing import Dict, List, Any, Optional

# Import from parent utils directory
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils import CommonUtils, CommonUtilsConstants
from . import AirflowUtilsConstants


def list_all_mwaa_environments(environment: str, region: str) -> Dict[str, Any]:
    """
    Lists all MWAA environments in the specified AWS account/region with comprehensive details
    
    Args:
        environment (str): Target environment (dev/tst/prd)
        region (str): Target region (us/eu/jp)
    
    Returns:
        dict: Response in the format:
              {
                  "status": "SUCCESS/FAILED",
                  "result": {
                      "environments": [list of environment details],
                      "count": number_of_environments,
                      "region": "actual_aws_region",
                      "target_environment": "environment"
                  },
                  "error": "<Error message if FAILED>"
              }
    """
    try:
        print(f"Starting to list MWAA environments for environment: {environment}, region: {region}")
        
        # Validate inputs
        if environment not in AirflowUtilsConstants.VALID_ENVIRONMENTS:
            return {
                CommonUtilsConstants.STATUS_KEY: CommonUtilsConstants.FAILED_KEY,
                "error": f"Invalid environment: {environment}. Valid values: {AirflowUtilsConstants.VALID_ENVIRONMENTS}"
            }
        
        if region not in AirflowUtilsConstants.VALID_REGIONS:
            return {
                CommonUtilsConstants.STATUS_KEY: CommonUtilsConstants.FAILED_KEY,
                "error": f"Invalid region: {region}. Valid values: {AirflowUtilsConstants.VALID_REGIONS}"
            }
        
        # Get MWAA client using CommonUtils
        mwaa_client = CommonUtils.get_boto3_client(
            AirflowUtilsConstants.MWAA_KEY, 
            environment, 
            region
        )
        
        # List all MWAA environments
        print("Calling list_environments API")
        response = mwaa_client.list_environments(MaxResults=AirflowUtilsConstants.DEFAULT_MAX_RESULTS)
        
        environment_names = response.get(AirflowUtilsConstants.ENVIRONMENTS_KEY, [])
        print(f"Found {len(environment_names)} MWAA environments")
        
        # Get detailed information for each environment
        detailed_environments = []
        
        for env_name in environment_names:
            try:
                print(f"Getting details for environment: {env_name}")
                env_details = mwaa_client.get_environment(Name=env_name)
                
                env_info = env_details.get(AirflowUtilsConstants.ENVIRONMENT_KEY, {})
                
                # Extract comprehensive information
                environment_info = {
                    "name": env_name,
                    "status": env_info.get(AirflowUtilsConstants.STATUS_KEY),
                    "airflow_version": env_info.get(AirflowUtilsConstants.AIRFLOW_VERSION_KEY),
                    "environment_class": env_info.get(AirflowUtilsConstants.ENVIRONMENT_CLASS_KEY),
                    "max_workers": env_info.get(AirflowUtilsConstants.MAX_WORKERS_KEY),
                    "min_workers": env_info.get(AirflowUtilsConstants.MIN_WORKERS_KEY),
                    "schedulers": env_info.get(AirflowUtilsConstants.SCHEDULERS_KEY),
                    "webserver_access_mode": env_info.get(AirflowUtilsConstants.WEBSERVER_ACCESS_MODE_KEY),
                    "created_at": str(env_info.get(AirflowUtilsConstants.CREATED_AT_KEY, "")),
                    "source_bucket_arn": env_info.get(AirflowUtilsConstants.SOURCE_BUCKET_ARN_KEY),
                    "dag_s3_path": env_info.get(AirflowUtilsConstants.DAG_S3_PATH_KEY),
                    "execution_role_arn": env_info.get(AirflowUtilsConstants.EXECUTION_ROLE_ARN_KEY),
                    "service_role_arn": env_info.get(AirflowUtilsConstants.SERVICE_ROLE_ARN_KEY),
                    "webserver_url": env_info.get(AirflowUtilsConstants.WEBSERVER_URL_KEY),
                    "arn": env_info.get(AirflowUtilsConstants.ARN_KEY),
                    "tags": env_info.get(AirflowUtilsConstants.TAGS_KEY, {}),
                    "weekly_maintenance_window": env_info.get("WeeklyMaintenanceWindowStart"),
                    "kms_key": env_info.get("KmsKey"),
                    "requirements_s3_path": env_info.get("RequirementsS3Path"),
                    "plugins_s3_path": env_info.get("PluginsS3Path")
                }
                
                detailed_environments.append(environment_info)
                
            except ClientError as e:
                print(f"Could not get details for environment {env_name}: {str(e)}")
                detailed_environments.append({
                    "name": env_name,
                    "status": "UNKNOWN",
                    "error": f"Could not fetch details: {str(e)}"
                })
            except Exception as e:
                print(f"Unexpected error getting details for {env_name}: {str(e)}")
                detailed_environments.append({
                    "name": env_name,
                    "status": "UNKNOWN", 
                    "error": f"Unexpected error: {str(e)}"
                })
        
        result = {
            "environments": detailed_environments,
            "count": len(detailed_environments),
            "region": AirflowUtilsConstants.REGION_DETAILS[region]["region_name"],
            "target_environment": environment,
            "region_details": AirflowUtilsConstants.REGION_DETAILS[region]
        }
        
        print(f"Successfully listed {len(detailed_environments)} MWAA environments")
        
        return {
            CommonUtilsConstants.STATUS_KEY: CommonUtilsConstants.SUCCESS_KEY,
            CommonUtilsConstants.RESULT_KEY: result
        }
        
    except ClientError as e:
        error_message = f"AWS Client Error while listing MWAA environments: {str(e)}"
        print(error_message)
        print(traceback.format_exc())
        
        return {
            CommonUtilsConstants.STATUS_KEY: CommonUtilsConstants.FAILED_KEY,
            "error": error_message
        }
        
    except Exception as e:
        error_message = f"Error while listing MWAA environments: {str(e)}"
        print(error_message)
        print(traceback.format_exc())
        
        return {
            CommonUtilsConstants.STATUS_KEY: CommonUtilsConstants.FAILED_KEY,
            "error": error_message
        }


def create_variable(
    key: str,
    value: str,
    environment: str,
    region: str,
    airflow_environment_name: str
) -> dict:
    """
    Create or update a variable in an MWAA environment via the REST API.
    Prints result to the terminal.
    """
    try:
        mwaa_client = CommonUtils.get_boto3_client(
            AirflowUtilsConstants.MWAA_KEY, environment, region
        )
        request_params = {
            "Name": airflow_environment_name,
            "Path": "/variables",
            "Method": "POST",
            "Body": {
                "key": key,
                "value": value,
            }
        }
        print(f"Creating variable with params: {request_params}")

        response = mwaa_client.invoke_rest_api(**request_params)
        http_status = response.get('ResponseMetadata', {}).get('HTTPStatusCode', 'Unknown')
        print(f"HTTP Status: {http_status}")

        resp_body = response.get("ResponseBody")
        if resp_body:
            try:
                content = resp_body.read().decode("utf-8")
                print(f"Response Body: {content}")
            except Exception as e:
                print(f"Could not read response body: {e}")
                content = None
        else:
            content = None
            print("No response body from API.")

        if http_status == 200:
            print("✅ Variable created/updated successfully.")
        else:
            print("❌ Failed to create/update variable.")

        return {
            "status": "success" if http_status == 200 else "failed",
            "result": content,
            "error": None if http_status == 200 else f"API returned status {http_status}"
        }

    except Exception as ex:
        print(f"❌ Unable to create variable in Airflow: {ex}")
        return {
            "status": "failed",
            "result": None,
            "error": str(ex)
        }

def create_connection(
    connection_id: str,
    conn_type: str,
    description: str,
    host: str,
    login: str,
    password: str,
    schema: str,
    port: int,
    extra: str,
    environment: str,
    region: str,
    airflow_environment_name: str
) -> dict:
    """
    Create or update a connection in MWAA via Airflow REST API with explicit parameters.

    Args:
        connection_id: Connection ID
        conn_type: Connection type (e.g., 'postgres')
        description: Description of the connection
        host: Hostname
        login: Username
        password: Password
        schema: Database/schema
        port: Port number
        extra: Extra JSON string for additional params
        environment: Deployment environment (e.g., 'dev', 'prd')
        region: AWS region (e.g., 'us-east-1')
        airflow_environment_name: MWAA environment name

    Returns:
        dict with 'status', 'result', and 'error'
    """
    payload = {
        "connection_id": connection_id,
        "conn_type": conn_type,
        "description": description,
        "host": host,
        "login": login,
        "password": password,
        "schema": schema,
        "port": port,
        "extra": extra
    }

    try:
        mwaa_client = CommonUtils.get_boto3_client(
            AirflowUtilsConstants.MWAA_KEY, environment, region
        )

        request_params = {
            "Name": airflow_environment_name,
            "Path": "/connections",
            "Method": "POST",
            "Body": payload
        }

        print(f"Sending create connection request with payload: {payload}")

        response = mwaa_client.invoke_rest_api(**request_params)

        http_status = response.get('ResponseMetadata', {}).get('HTTPStatusCode', 'Unknown')
        print(f"HTTP response code: {http_status}")

        resp_body = response.get("ResponseBody")
        content = None
        if resp_body:
            content = resp_body.read().decode("utf-8")
            print(f"Response body: {content}")

        if http_status == 200:
            print("✅ Connection created or updated successfully.")
            return {"status": "success", "result": content, "error": None}
        else:
            print("❌ Failed to create or update connection.")
            return {"status": "failed", "result": content, "error": f"HTTP {http_status}"}

    except Exception as e:
        print(f"❌ Exception during creating connection: {e}")
        return {"status": "failed", "result": None, "error": str(e)}
