"""
Utils package for automation project
Contains common utilities for Vault, AWS, and general automation tasks
"""

from .CommonUtils import (
    get_config,
    client_auth,
    read_secret,
    get_boto3_client,
    get_aws_region,
    assume_cross_account_role,
    get_current_environment,
    get_current_region,
    get_secret_engine
)

from . import CommonUtilsConstants

# from .DLPLogSetup import get_logger

__all__ = [
    # CommonUtils functions
    'get_config',
    'client_auth',
    'read_secret',
    'get_boto3_client',
    'get_aws_region',
    'assume_cross_account_role',
    'get_current_environment',
    'get_current_region',
    'get_secret_engine',
    
    # Constants module
    'CommonUtilsConstants',
    
    # Logger (uncomment when you add it)
    # 'get_logger'
]
