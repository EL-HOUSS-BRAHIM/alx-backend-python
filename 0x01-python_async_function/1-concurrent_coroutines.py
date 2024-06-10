#!/usr/bin/env python3
""" 1. Let's execute multiple coroutines at the same time with async"""
import asyncio
from typing import List
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> float:
    '''
    Asynchronous coroutine that takes in two integers arguments
    and returns a float.
    '''
    delay = 0
    tasks = []
    for _ in range(n):
        tasks.append(asyncio.create_task(wait_random(max_delay)))
    for task in tasks:
        delay += await task
    return delay
