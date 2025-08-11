#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = "ZS Associates"

"""
AirflowUtilsConstants.py - Constants for Airflow Utilities
Incorporates constants from the main AirflowAutomationConstants
"""

# Import your existing region details and other constants
REGION_DETAILS = {
    "us": {
        "region_name": "us-east-1",
        "location_char": "VGA",
        "network_configuration": {
            "dev": {
                "SubnetIds": [
                    "subnet-0358a1fd3812cd25c",
                    "subnet-03fefe8d468ba890a"
                ],
                "SecurityGroupIds": [
                    "sg-0883892898b9b8815"
                ],
            },
            "tst": {
                "SubnetIds": [
                    "subnet-03bcedea2c0b6df45",
                    "subnet-079ded96b7220b7ac"
                ],
                "SecurityGroupIds": [
                    "sg-053cfafc675797fdf"
                ]
            },
            "prd": {
                "SubnetIds": [
                    "subnet-0cb0858a298b3a8d2",
                    "subnet-099eaed7c619a940c"
                ],
                "SecurityGroupIds": [
                    "sg-01afd887dfc2f130d"
                ]
            }
        }
    },
    "jp": {
        "region_name": "ap-northeast-1",
        "location_char": "TYO",
        "network_configuration": {
            "dev": {
                "SubnetIds": [
                    "subnet-00603300e130d701a",
                    "subnet-039865fc23bf4eaf8"
                ],
                "SecurityGroupIds": [
                    "sg-0653c1254d441bced"
                ]
            },
            "tst": {
                "SubnetIds": [
                    "subnet-0fbaf541175acd62a",
                    "subnet-032bc201d7403a422"
                ],
                "SecurityGroupIds": [
                    "sg-074f245e3fe6a5863"
                ]
            },
            "prd": {
                "SubnetIds": [
                    "subnet-0b79c5fd06fd3ec65",
                    "subnet-000689fb4780e054d"
                ],
                "SecurityGroupIds": [
                    "sg-07ee91ad2a9de9f83"
                ]
            }
        }
    },
    "eu": {
        "region_name": "eu-central-1",
        "location_char": "FRA",
        "network_configuration": {
            "dev": {
                "SubnetIds": [
                    "subnet-0d5f2beea20c4e719",
                    "subnet-0676ab54949662b68"
                ],
                "SecurityGroupIds": [
                    "sg-0264ac0c4c6718098"
                ]
            },
            "tst": {
                "SubnetIds": [
                    "subnet-08d78fb2afd6c26f8",
                    "subnet-0ffef800ad8db4fc4"
                ],
                "SecurityGroupIds": [
                    "sg-05b926103d9bfebc1"
                ]
            },
            "prd": {
                "SubnetIds": [
                    "subnet-0e23bd78e7acfaf52",
                    "subnet-0b6a03b1d53cf4d19"
                ],
                "SecurityGroupIds": [
                    "sg-091417c26e237b252"
                ]
            }
        }
    }
}

LOGGING_CONFIGURATIONS = {
    "DagProcessingLogs": {
        "LogLevel": "INFO",
        "Enabled": True
    },
    "SchedulerLogs": {
        "LogLevel": "INFO",
        "Enabled": True
    },
    "TaskLogs": {
        "LogLevel": "INFO",
        "Enabled": True
    },
    "WebserverLogs": {
        "LogLevel": "INFO",
        "Enabled": True
    },
    "WorkerLogs": {
        "LogLevel": "INFO",
        "Enabled": True
    }
}

ENVIRONMENT_CLASS = {
    "small": {
        "EnvironmentClass": "mw1.small",
        "MaxWorkers": 10,
        "MinWorkers": 1,
        "Schedulers": 2,
        "MinWebservers": 2,
        "MaxWebservers": 2,
    },
    "medium": {
        "EnvironmentClass": "mw1.medium",
        "MaxWorkers": 10,
        "MinWorkers": 1,
        "Schedulers": 2,
        "MinWebservers": 2,
        "MaxWebservers": 2,
    },
    "large": {
        "EnvironmentClass": "mw1.large",
        "MaxWorkers": 10,
        "MinWorkers": 1,
        "Schedulers": 2,
        "MinWebservers": 2,
        "MaxWebservers": 2,
    }
}

# AWS Service Keys
MWAA_KEY = "mwaa"
IAM_KEY = "iam"
CLOUDWATCH_KEY = "cloudwatch"

# API Paths for MWAA REST API
VARIABLES_PATH = "/variables"
CONNECTIONS_PATH = "/connections"

# HTTP Methods
GET_METHOD = "GET"
POST_METHOD = "POST"
PUT_METHOD = "PUT"
DELETE_METHOD = "DELETE"

# Response Keys
ENVIRONMENTS_KEY = "Environments"
ENVIRONMENT_KEY = "Environment"

# Environment Status
AIRFLOW_STATUS_AVAILABLE_KEY = "AVAILABLE"
AIRFLOW_STATUS_FAILED_KEY = "CREATE_FAILED"
STATUS_CREATING = "CREATING"
STATUS_DELETING = "DELETING"
STATUS_UPDATING = "UPDATING"
STATUS_UPDATE_FAILED = "UPDATE_FAILED"

# Environment Details Keys
NAME_KEY = "Name"
STATUS_KEY = "Status"
AIRFLOW_VERSION_KEY = "AirflowVersion"
ENVIRONMENT_CLASS_KEY = "EnvironmentClass"
MAX_WORKERS_KEY = "MaxWorkers"
MIN_WORKERS_KEY = "MinWorkers"
SCHEDULERS_KEY = "Schedulers"
WEBSERVER_ACCESS_MODE_KEY = "WebserverAccessMode"
CREATED_AT_KEY = "CreatedAt"
LAST_UPDATE_KEY = "LastUpdate"
SOURCE_BUCKET_ARN_KEY = "SourceBucketArn"
DAG_S3_PATH_KEY = "DagS3Path"
EXECUTION_ROLE_ARN_KEY = "ExecutionRoleArn"
SERVICE_ROLE_ARN_KEY = "ServiceRoleArn"
WEBSERVER_URL_KEY = "WebserverUrl"
ARN_KEY = "Arn"
TAGS_KEY = "Tags"

# Network Configuration Keys
NETWORK_CONFIGURATION_KEY = "NetworkConfiguration"
VPC_ID_KEY = "VpcId"
SUBNET_IDS_KEY = "SubnetIds"
SECURITY_GROUP_IDS_KEY = "SecurityGroupIds"

# Variable Response Keys
VARIABLES_RESPONSE_KEY = "variables"
VARIABLE_KEY_KEY = "key"
VARIABLE_VALUE_KEY = "value"

# Connection Response Keys
CONNECTIONS_RESPONSE_KEY = "connections"
CONNECTION_ID_KEY = "conn_id"
CONNECTION_TYPE_KEY = "conn_type"
DESCRIPTION_KEY = "description"
HOST_KEY = "host"
LOGIN_KEY = "login"
SCHEMA_KEY = "schema"
PORT_KEY = "port"
EXTRA_KEY = "extra"

# Environment and Region Keys
DEV_ENV_KEY = "dev"
TST_ENV_KEY = "tst"
PRD_ENV_KEY = "prd"
VALID_ENVIRONMENTS = ["dev", "tst", "prd"]
VALID_REGIONS = ["us", "eu", "jp"]

# MWAA Configuration Keys
DAG_S3_PATH = "dags/"
PLUGINS_S3_PATH = "plugins"
REQUIREMENTS_S3_PATH = "requirements.txt"
WEB_SERVER_ACCESS_MODE = "PUBLIC_ONLY"
WEEKLY_MAINTENANCE_WINDOW_START = "SAT:22:00"

# Log Groups
LOG_GROUPS = ["Task", "Scheduler", "DAGProcessing", "WebServer", "Worker"]

# Validation Keys
EMAIL_VALIDATION = "@takeda.com"
APMS_ID_VALIDATION = "APMS-"
VALID_ENVIRONMENT_SIZE = ["small", "medium", "large"]

# Timeout and Sleep
TIMEOUT_KEY = 2700
SLEEP_TIME_KEY = 30

# Error Messages
ERROR_NO_ENVIRONMENTS = "No MWAA environments found"
ERROR_ENVIRONMENT_NOT_FOUND = "Environment not found"
ERROR_GETTING_VARIABLES = "Error getting variables"
ERROR_GETTING_CONNECTIONS = "Error getting connections"
ERROR_INVALID_ENVIRONMENT = "Invalid environment parameter"
ERROR_INVALID_REGION = "Invalid region parameter"

# Success Messages
SUCCESS_ENVIRONMENTS_LISTED = "Successfully listed MWAA environments"
SUCCESS_VARIABLES_RETRIEVED = "Successfully retrieved variables"
SUCCESS_CONNECTIONS_RETRIEVED = "Successfully retrieved connections"

# Airflow Environment Naming
AIRFLOW_ENVIRONMENT_NAME = "MWAA1{region}{location}{apms_id}{environment}{id}"
REGION_NAME_KEY = "region_name"
LOCATION_CHAR_KEY = "location_char"

# Version and Configuration Keys
VERSION_KEY = "airflow_version"
ENVIRONMENT_NAME_KEY = "environment_name"

# Pagination
NEXT_TOKEN_KEY = "NextToken"
MAX_RESULTS_KEY = "MaxResults"
DEFAULT_MAX_RESULTS = 25
