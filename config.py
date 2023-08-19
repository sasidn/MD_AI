# config.py

# Replace the placeholders with your actual MySQL credentials
MYSQL_USERNAME = 'MindNex'
MYSQL_PASSWORD = 'MindNex'
MYSQL_HOST = 'localhost'
MYSQL_PORT = '3306'
MYSQL_DATABASE = 'MindNex'

# Construct the connection string
DATABASE_URI = f'mysql+mysqlconnector://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
