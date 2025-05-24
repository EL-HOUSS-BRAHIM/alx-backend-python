#!/usr/bin/env python3
"""Module for implementing retry mechanism for database operations."""
import time
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
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper


def retry_on_failure(retries: int = 3, delay: int = 2) -> Callable:
    """
    Decorator that retries a function call on failure.
    
    Args:
        retries: Number of retry attempts
        delay: Delay in seconds between retries
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == retries:
                        raise e
                    time.sleep(delay)
            return None
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn) -> list:
    """Fetch all users with retry mechanism."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


if __name__ == "__main__":
    # Example usage
    users = fetch_users_with_retry()
    print(users)
