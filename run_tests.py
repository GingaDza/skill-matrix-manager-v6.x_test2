#!/usr/bin/env python3

import pytest
import sys
import os
from datetime import datetime

def set_test_environment():
    """テスト環境変数の設定"""
    os.environ['SKILL_MATRIX_TEST_USER'] = 'GingaDza'
    os.environ['SKILL_MATRIX_TEST_TIME'] = '2025-02-19 20:24:33'
    os.environ['SKILL_MATRIX_TEST_MODE'] = 'True'

def run_tests():
    """テストの実行"""
    set_test_environment()
    
    if not os.path.exists('tests'):
        print("Error: 'tests' directory not found")
        sys.exit(1)
    
    pytest_args = [
        'tests/',
        '-v',
        '--cov=src/skill_matrix_manager',
        '--cov-report=term-missing',
        '--cov-report=html',
    ]
    
    if '--ui-tests' in sys.argv:
        pytest_args.extend(['-m', 'ui'])
    
    try:
        exit_code = pytest.main(pytest_args)
        
        if exit_code == 0:
            print("\nAll tests passed successfully!")
        else:
            print("\nSome tests failed. Check the output above for details.")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error running tests: {e}")
        sys.exit(1)

def main():
    current_time = os.environ.get('SKILL_MATRIX_TEST_TIME', '2025-02-19 20:24:33')
    current_user = os.environ.get('SKILL_MATRIX_TEST_USER', 'GingaDza')
    
    print(f"Starting tests at {current_time}")
    print(f"Test user: {current_user}")
    
    try:
        run_tests()
    except KeyboardInterrupt:
        print("\nTest execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError during test execution: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
