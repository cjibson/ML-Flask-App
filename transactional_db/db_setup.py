import psycopg2
from db_keys import db_config

def connect_to_db():
    try:
        connection = psycopg2.connect(**db_config)
        print("Connection to database established successfully.")
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

# Example usage
if __name__ == "__main__":
    connection = connect_to_db()
    if connection:
        # Perform database operations here
        connection.close()
