#!/usr/bin/env python3
""" 0.async generator"""
import asyncio
import random
from typing import AsyncGenerator


async def async_generator() -> AsyncGenerator[float, None, None]:
    """async generator"""
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.random(0, 10)
