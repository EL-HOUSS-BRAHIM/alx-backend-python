#!/usr/bin/env python3
"""Module for concurrent asynchronous database operations."""
import asyncio
import aiosqlite
from typing import List, Tuple, Any


async def async_fetch_users() -> List[Tuple[Any, ...]]:
    """Fetch all users asynchronously."""
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()


async def async_fetch_older_users() -> List[Tuple[Any, ...]]:
    """Fetch users older than 40 asynchronously."""
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            return await cursor.fetchall()


async def fetch_concurrently() -> Tuple[List[Tuple[Any, ...]], List[Tuple[Any, ...]]]:
    """Execute both queries concurrently."""
    return await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )


if __name__ == "__main__":
    # Run both queries concurrently
    all_users, older_users = asyncio.run(fetch_concurrently())
    print("All users:", all_users)
    print("Users older than 40:", older_users)
