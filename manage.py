import os
import sys
from dotenv import load_dotenv

load_dotenv()

def main():
    """
    Main entry point for Django. Loads environment variables and sets up application.
    :return:
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_config.deployment')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as import_error:
        raise(
            'Could not import Django. Make sure it is installed and'
            'available on your PYTHONPATH environment variable.'
            'Or maybe you forgot to activate your virtual environment?'
        ) from import_error

    execute_from_command_line(sys.argv)


if __name__=='__main__':
    main()