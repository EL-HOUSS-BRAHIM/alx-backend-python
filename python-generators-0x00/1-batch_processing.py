#!/usr/bin/python3
"""Module for batch processing user data."""
from seed import connect_to_prodev


def stream_users_in_batches(batch_size):
    """Generator that fetches users in batches."""
    connection = connect_to_prodev()
    if not connection:
        return

    try:
        cursor = connection.cursor(dictionary=True)
        offset = 0
        
        while True:
            cursor.execute(f"""
                SELECT * FROM user_data 
                LIMIT {batch_size} OFFSET {offset}
            """)
            batch = cursor.fetchall()
            if not batch:
                break
            yield batch
            offset += batch_size

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()


def batch_processing(batch_size):
    """Process users in batches and filter those over age 25."""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
