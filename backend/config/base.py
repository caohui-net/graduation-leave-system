"""
Base configuration for all environments
"""
import os

# Feature Flags
FEATURE_FLAGS = {
    'stay_school_approval': os.getenv('ENABLE_STAY_SCHOOL', 'false').lower() == 'true',
    'leave_request_approval': os.getenv('ENABLE_LEAVE_REQUEST', 'false').lower() == 'true',
}
