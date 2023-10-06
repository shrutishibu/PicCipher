import os

# Check for DJANGO_DB_HOST environment variable
db_host = os.environ.get('DJANGO_DB_HOST')
if db_host:
    print(f'DJANGO_DB_HOST is set to: {db_host}')
else:
    print('DJANGO_DB_HOST is not set.')

# Repeat this process for other environment variables (DJANGO_DB_USER, DJANGO_DB_PASSWORD, DJANGO_DB_NAME, etc.)
