#!/usr/bin/python3
"""Module for memory-efficient age aggregation."""
from seed import connect_to_prodev


def stream_user_ages():
    """Generator that yields user ages one by one."""
    connection = connect_to_prodev()
    if not connection:
        return

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")
        
        for (age,) in cursor:
            yield age

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()


def calculate_average_age():
    """Calculate average age using the generator."""
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count > 0:
        average_age = total_age / count
        print(f"Average age of users: {average_age:.2f}")
    else:
        print("No users found in database")
