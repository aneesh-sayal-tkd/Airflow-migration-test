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


def get_environment_variables(environment: str, region: str, airflow_environment_name: str) -> Dict[str, Any]:
    """
    Get all variables from a specific MWAA environment using REST API
    
    Args:
        environment (str): Target environment (dev/tst/prd)
        region (str): Target region (us/eu/jp)
        airflow_environment_name (str): Name of the MWAA environment
    
    Returns:
        dict: Response with variables information
    """
    try:
        print(f"Getting variables for MWAA environment: {airflow_environment_name}")
        
        # Validate inputs
        if environment not in AirflowUtilsConstants.VALID_ENVIRONMENTS:
            return {
                CommonUtilsConstants.STATUS_KEY: CommonUtilsConstants.FAILED_KEY,
                "error": f"Invalid environment: {environment}"
            }
        
        if region not in AirflowUtilsConstants.VALID_REGIONS:
            return {
                CommonUtilsConstants.STATUS_KEY: CommonUtilsConstants.FAILED_KEY,
                "error": f"Invalid region: {region}"
            }
        
        # Get MWAA client
        mwaa_client = CommonUtils.get_boto3_client(
            AirflowUtilsConstants.MWAA_KEY, 
            environment, 
            region
        )
        
        # Use MWAA REST API to get variables
        request_params = {
            AirflowUtilsConstants.NAME_KEY: airflow_environment_name,
            "Path": AirflowUtilsConstants.VARIABLES_PATH,
            "Method": AirflowUtilsConstants.GET_METHOD
        }
        
        print(f"Invoking REST API with params: {request_params}")
        response = mwaa_client.invoke_rest_api(**request_params)
        
        # Parse the response
        if response.get('ResponseBody'):
            response_data = json.loads(response['ResponseBody'].read().decode('utf-8'))
            print(f"API Response: {response_data}")
            
            variables_list = []
            
            # Handle different response formats
            if isinstance(response_data, dict):
                # Check for variables key
                if AirflowUtilsConstants.VARIABLES_RESPONSE_KEY in response_data:
                    variables_data = response_data[AirflowUtilsConstants.VARIABLES_RESPONSE_KEY]
                    
                    if isinstance(variables_data, list):
                        variables_list = variables_data
                    elif isinstance(variables_data, dict):
                        # Convert dict to list format
                        variables_list = [
                            {
                                AirflowUtilsConstants.VARIABLE_KEY_KEY: key,
                                AirflowUtilsConstants.VARIABLE_VALUE_KEY: value
                            }
                            for key, value in variables_data.items()
                        ]
                # Check if response_data itself contains variables directly
                elif isinstance(response_data, dict) and all(isinstance(v, (str, int, float, bool)) for v in response_data.values()):
                    variables_list = [
                        {
                            AirflowUtilsConstants.VARIABLE_KEY_KEY: key,
                            AirflowUtilsConstants.VARIABLE_VALUE_KEY: value
                        }
                        for key, value in response_data.items()
                    ]
            
            result = {
                "environment_name": airflow_environment_name,
                "variables": variables_list,
                "variables_count": len(variables_list),
                "region": AirflowUtilsConstants.REGION_DETAILS[region]["region_name"],
                "target_environment": environment,
                "raw_response": response_data  # Include for debugging
            }
            
            print(f"Successfully retrieved {len(variables_list)} variables")
            
            return {
                CommonUtilsConstants.STATUS_KEY: CommonUtilsConstants.SUCCESS_KEY,
                CommonUtilsConstants.RESULT_KEY: result
            }
        else:
            return {
                CommonUtilsConstants.STATUS_KEY: CommonUtilsConstants.FAILED_KEY,
                "error": "No response body received from MWAA API"
            }
        
    except ClientError as e:
        error_message = f"AWS Client Error while getting variables: {str(e)}"
        print(error_message)
        
        return {
            CommonUtilsConstants.STATUS_KEY: CommonUtilsConstants.FAILED_KEY,
            "error": error_message
        }
        
    except Exception as e:
        error_message = f"Error while getting variables: {str(e)}"
        print(error_message)
        print(traceback.format_exc())
        
        return {
            CommonUtilsConstants.STATUS_KEY: CommonUtilsConstants.FAILED_KEY,
            "error": error_message
        }
    

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
            
    except ClientError as e:
        print(f"InvokeRestApi failed: {e.response}")
        raise
    except Exception as ex:
        status_message = f"Unable to get variable from airflow env: {str(ex)}"
        print(status_message)
        raise Exception(status_message)


def get_environment_connections(environment: str, region: str, airflow_environment_name: str) -> Dict[str, Any]:
    """
    Get all connections from a specific MWAA environment using REST API
    
    Args:
        environment (str): Target environment (dev/tst/prd)
        region (str): Target region (us/eu/jp)
        airflow_environment_name (str): Name of the MWAA environment
    
    Returns:
        dict: Response with connections information
    """
    try:
        print(f"Getting connections for MWAA environment: {airflow_environment_name}")
        
        # Validate inputs
        if environment not in AirflowUtilsConstants.VALID_ENVIRONMENTS:
            return {
                CommonUtilsConstants.STATUS_KEY: CommonUtilsConstants.FAILED_KEY,
                "error": f"Invalid environment: {environment}"
            }
        
        if region not in AirflowUtilsConstants.VALID_REGIONS:
            return {
                CommonUtilsConstants.STATUS_KEY: CommonUtilsConstants.FAILED_KEY,
                "error": f"Invalid region: {region}"
            }
        
        # Get MWAA client
        mwaa_client = CommonUtils.get_boto3_client(
            AirflowUtilsConstants.MWAA_KEY, 
            environment, 
            region
        )
        
        # Use MWAA REST API to get connections
        request_params = {
            AirflowUtilsConstants.NAME_KEY: airflow_environment_name,
            "Path": AirflowUtilsConstants.CONNECTIONS_PATH,
            "Method": AirflowUtilsConstants.GET_METHOD
        }
        
        print(f"Invoking REST API with params: {request_params}")
        response = mwaa_client.invoke_rest_api(**request_params)
        
        # Parse the response
        if response.get('ResponseBody'):
            response_data = json.loads(response['ResponseBody'].read().decode('utf-8'))
            print(f"API Response: {response_data}")
            
            connections_list = []
            
            if isinstance(response_data, dict) and AirflowUtilsConstants.CONNECTIONS_RESPONSE_KEY in response_data:
                connections_data = response_data[AirflowUtilsConstants.CONNECTIONS_RESPONSE_KEY]
                
                if isinstance(connections_data, list):
                    for conn in connections_data:
                        connection_info = {
                            AirflowUtilsConstants.CONNECTION_ID_KEY: conn.get(AirflowUtilsConstants.CONNECTION_ID_KEY),
                            AirflowUtilsConstants.CONNECTION_TYPE_KEY: conn.get(AirflowUtilsConstants.CONNECTION_TYPE_KEY),
                            AirflowUtilsConstants.DESCRIPTION_KEY: conn.get(AirflowUtilsConstants.DESCRIPTION_KEY),
                            AirflowUtilsConstants.HOST_KEY: conn.get(AirflowUtilsConstants.HOST_KEY),
                            AirflowUtilsConstants.LOGIN_KEY: conn.get(AirflowUtilsConstants.LOGIN_KEY),
                            AirflowUtilsConstants.SCHEMA_KEY: conn.get(AirflowUtilsConstants.SCHEMA_KEY),
                            AirflowUtilsConstants.PORT_KEY: conn.get(AirflowUtilsConstants.PORT_KEY),
                            AirflowUtilsConstants.EXTRA_KEY: conn.get(AirflowUtilsConstants.EXTRA_KEY),
                            "is_encrypted": conn.get("is_encrypted"),
                            "is_extra_encrypted": conn.get("is_extra_encrypted")
                        }
                        connections_list.append(connection_info)
            
            result = {
                "environment_name": airflow_environment_name,
                "connections": connections_list,
                "connections_count": len(connections_list),
                "region": AirflowUtilsConstants.REGION_DETAILS[region]["region_name"],
                "target_environment": environment,
                "raw_response": response_data  # Include for debugging
            }
            
            print(f"Successfully retrieved {len(connections_list)} connections")
            
            return {
                CommonUtilsConstants.STATUS_KEY: CommonUtilsConstants.SUCCESS_KEY,
                CommonUtilsConstants.RESULT_KEY: result
            }
        else:
            return {
                CommonUtilsConstants.STATUS_KEY: CommonUtilsConstants.FAILED_KEY,
                "error": "No response body received from MWAA API"
            }
        
    except ClientError as e:
        error_message = f"AWS Client Error while getting connections: {str(e)}"
        print(error_message)
        
        return {
            CommonUtilsConstants.STATUS_KEY: CommonUtilsConstants.FAILED_KEY,
            "error": error_message
        }
        
    except Exception as e:
        error_message = f"Error while getting connections: {str(e)}"
        print(error_message)
        print(traceback.format_exc())
        
        return {
            CommonUtilsConstants.STATUS_KEY: CommonUtilsConstants.FAILED_KEY,
            "error": error_message
        }


def get_environment_summary_by_region(environment: str, region: str) -> Dict[str, Any]:
    """
    Get a summary of MWAA environments with region-specific network details
    
    Args:
        environment (str): Target environment (dev/tst/prd)
        region (str): Target region (us/eu/jp)
    
    Returns:
        dict: Response with environment summary and region configuration
    """
    try:
        print(f"Getting environment summary for region: {region}, environment: {environment}")
        
        # Get basic environment list first
        envs_result = list_all_mwaa_environments(environment, region)
        
        if envs_result[CommonUtilsConstants.STATUS_KEY] != CommonUtilsConstants.SUCCESS_KEY:
            return envs_result
        
        environments = envs_result[CommonUtilsConstants.RESULT_KEY]["environments"]
        
        # Add region-specific information
        region_config = AirflowUtilsConstants.REGION_DETAILS.get(region, {})
        network_config = region_config.get("network_configuration", {}).get(environment, {})
        
        summary = {
            "region_info": {
                "region_code": region,
                "region_name": region_config.get("region_name"),
                "location_char": region_config.get("location_char"),
                "network_configuration": network_config
            },
            "environment_summary": {
                "total_environments": len(environments),
                "available_environments": len([env for env in environments if env.get("status") == AirflowUtilsConstants.AIRFLOW_STATUS_AVAILABLE_KEY]),
                "creating_environments": len([env for env in environments if env.get("status") == AirflowUtilsConstants.STATUS_CREATING]),
                "failed_environments": len([env for env in environments if env.get("status") == AirflowUtilsConstants.AIRFLOW_STATUS_FAILED_KEY])
            },
            "environments": [
                {
                    "name": env.get("name"),
                    "status": env.get("status"),
                    "environment_class": env.get("environment_class"),
                    "airflow_version": env.get("airflow_version"),
                    "webserver_url": env.get("webserver_url")
                }
                for env in environments
            ]
        }
        
        return {
            CommonUtilsConstants.STATUS_KEY: CommonUtilsConstants.SUCCESS_KEY,
            CommonUtilsConstants.RESULT_KEY: summary
        }
        
    except Exception as e:
        error_message = f"Error while getting environment summary: {str(e)}"
        print(error_message)
        
        return {
            CommonUtilsConstants.STATUS_KEY: CommonUtilsConstants.FAILED_KEY,
            "error": error_message
        }
