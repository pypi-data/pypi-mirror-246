import os
import sys

def check_environment_variables():
    required_variables = [
        'GENIUS_API_URL',
        'GENIUS_API_LOGIN',
        'GENIUS_API_PASSWORD',
        'GENIUS_API_COMPANY_CODE',
        'AXYA_API_URL',
        'AXYA_API_TOKEN',
    ]
    is_missing = False
    for variable in required_variables:
        if not os.environ.get(variable):
            print(f"Environment variable {variable} is not set. Please set it.")
            is_missing = True

    if is_missing:
        try:
            sys.exit(1)
        except SystemExit as e:
            sys.exit(e.code)

if __name__ == '__main__':
    check_environment_variables()
    print("All required environment variables are set.")
