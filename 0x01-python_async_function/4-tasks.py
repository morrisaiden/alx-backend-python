#!/usr/bin/env python3
"""
Execute multiple coroutines at the same time with async
"""
from typing import List
import asyncio
task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """_summary_

    Args:
        n (int): _description_
        max_delay (int): _description_

    Returns:
        List[float]: _description_
    """
    futures = [task_wait_random(max_delay) for _ in range(n)]
    futures = asyncio.as_completed(futures)
    delays = [await futures for futures in futures]
    return delays
