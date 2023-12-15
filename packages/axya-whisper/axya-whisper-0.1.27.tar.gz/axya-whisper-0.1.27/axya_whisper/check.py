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

    for variable in required_variables:
        if not os.environ.get(variable):
            print(f"Environment variable {variable} is not set. Please set it.")
            sys.exit(1)

if __name__ == '__main__':
    check_environment_variables()
    print("All required environment variables are set.")
