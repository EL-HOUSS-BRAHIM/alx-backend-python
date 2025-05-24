#!/usr/bin/env python3
"""Module for ExecuteQuery context manager."""
import sqlite3
from typing import Any, List, Tuple


class ExecuteQuery:
    """A context manager for executing database queries."""

    def __init__(self, query: str, params: tuple = ()):
        """Initialize with query and parameters."""
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self) -> List[Tuple[Any, ...]]:
        """Execute query when entering context and return results."""
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close database resources when exiting context."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        return False


if __name__ == "__main__":
    # Example usage of the context manager
    with ExecuteQuery("SELECT * FROM users WHERE age > ?", (25,)) as results:
        print(results)
