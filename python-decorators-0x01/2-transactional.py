#!/usr/bin/env python3
"""Module for managing database transactions using decorators."""
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


def transactional(func: Callable) -> Callable:
    """
    Decorator that manages database transactions.
    Automatically commits changes if successful or rolls back if an error occurs.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            raise e  # Re-raise the exception after rollback
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id: int, new_email: str) -> None:
    """Update a user's email address."""
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", 
                  (new_email, user_id))


if __name__ == "__main__":
    # Example usage
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
