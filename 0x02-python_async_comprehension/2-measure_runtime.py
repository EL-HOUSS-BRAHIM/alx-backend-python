#!/usr/bin/env python3
""" 2. Run time for four parallel comprehensions """
import asyncio
from typing import List
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """ Measure runtime """
    start = asyncio.get_event_loop().time()
    await async_comprehension()
    end = asyncio.get_event_loop().time()
    return end - start
