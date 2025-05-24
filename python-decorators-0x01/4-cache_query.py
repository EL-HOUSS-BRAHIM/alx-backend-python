#!/usr/bin/env python3
"""Module for implementing query caching using decorators."""
import time
import sqlite3
import functools
from typing import Callable, Dict, Any

# Global cache dictionary to store query results
query_cache: Dict[str, Any] = {}


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


def cache_query(func: Callable) -> Callable:
    """
    Decorator that caches query results.
    Results are cached based on the SQL query string.
    """
    @functools.wraps(func)
    def wrapper(conn, query: str, *args, **kwargs):
        # Use the query string as the cache key
        if query in query_cache:
            return query_cache[query]
        
        # Execute the query and cache the result
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query: str) -> list:
    """Fetch users with caching mechanism."""
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


if __name__ == "__main__":
    # Example usage
    # First call will execute the query and cache the result
    users = fetch_users_with_cache(query="SELECT * FROM users")
    
    # Second call will use the cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print("Both calls return the same result:", users == users_again)
