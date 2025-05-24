#!/usr/bin/python3
"""Module for lazy pagination of user data."""
from seed import connect_to_prodev


def paginate_users(page_size, offset):
    """Fetch a page of users from the database."""
    connection = connect_to_prodev()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"""
            SELECT * FROM user_data 
            LIMIT {page_size} OFFSET {offset}
        """)
        rows = cursor.fetchall()
        return rows
    finally:
        cursor.close()
        connection.close()


def lazy_paginate(page_size):
    """Generator for lazy loading paginated data."""
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
