#!/usr/bin/env python3
"""Module for logging database queries using decorators."""
import sqlite3
import functools
from typing import Callable
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

def log_queries() -> Callable:
    """Decorator that logs database queries before execution."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Log the query if it's passed as a keyword argument
            query = kwargs.get('query', args[0] if args else None)
            if query:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                logging.info(f"[{timestamp}] Executing query: {query}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@log_queries()
def fetch_all_users(query: str) -> list:
    """Fetch all users from the database."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    # Example usage
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
