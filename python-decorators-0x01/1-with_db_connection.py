#!/usr/bin/env python3
"""Module for handling database connections using decorators."""
import sqlite3
import functools
from typing import Callable


def with_db_connection(func: Callable) -> Callable:
    """
    Decorator that handles database connections automatically.
    Opens a connection, passes it to the function, and ensures proper closure.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            # Pass the connection as the first argument to the decorated function
            result = func(conn, *args, **kwargs)
            return result
        finally:
            # Ensure connection is always closed, even if an error occurs
            conn.close()
    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id: int) -> tuple:
    """Get a user by their ID from the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


if __name__ == "__main__":
    # Example usage
    user = get_user_by_id(user_id=1)
    print(user)
