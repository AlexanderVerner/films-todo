#!/usr/bin/env python3
"""Validate that POSTGRES_PASSWORD is properly externalized (not hardcoded in docker-compose.yml)"""

import os
import re
import sys

def check_docker_compose_no_hardcoded_password():
    """Ensure docker-compose.yml doesn't contain hardcoded postgres password"""
    with open('docker-compose.yml', 'r') as f:
        content = f.read()
    
    # Check for hardcoded password pattern (alphanumeric string after POSTGRES_PASSWORD:)
    # Should be ${POSTGRES_PASSWORD} instead
    hardcoded_pattern = r'POSTGRES_PASSWORD:\s+[a-zA-Z0-9]+'
    if re.search(hardcoded_pattern, content):
        print("❌ FAIL: Hardcoded POSTGRES_PASSWORD found in docker-compose.yml")
        return False
    
    # Check for variable reference
    if '${POSTGRES_PASSWORD}' not in content:
        print("❌ FAIL: POSTGRES_PASSWORD variable not found in docker-compose.yml")
        return False
    
    print("✓ PASS: POSTGRES_PASSWORD properly externalized to environment variables")
    return True

def check_env_files_exist():
    """Verify env files exist"""
    files = ['_local_deploy/common.env', '.env']
    for f in files:
        if os.path.exists(f):
            print(f"✓ {f} exists")
        else:
            print(f"⚠ {f} not found (but may be in .gitignore)")
    return True

if __name__ == '__main__':
    success = check_docker_compose_no_hardcoded_password() and check_env_files_exist()
    sys.exit(0 if success else 1)
