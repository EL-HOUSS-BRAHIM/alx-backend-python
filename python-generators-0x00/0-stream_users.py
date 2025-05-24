#!/usr/bin/python3
"""Module for streaming users from database."""
from seed import connect_to_prodev


def stream_users():
    """Generator function that streams user data one row at a time."""
    connection = connect_to_prodev()
    if not connection:
        return

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        
        for row in cursor:
            yield row

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()
