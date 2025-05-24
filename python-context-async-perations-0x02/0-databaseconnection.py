#!/usr/bin/env python3
"""Module for DatabaseConnection context manager."""
import sqlite3


class DatabaseConnection:
    """A context manager for database connections."""

    def __init__(self, db_name: str = 'users.db'):
        """Initialize with database name."""
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Open database connection when entering context."""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close database connection when exiting context."""
        if self.conn:
            self.conn.close()
        return False


if __name__ == "__main__":
    # Example usage of the context manager
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)
