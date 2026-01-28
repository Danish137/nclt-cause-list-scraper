import asyncio

async def retry_async(fn, retries=3, delay=1):
    for attempt in range(retries):
        try:
            return await fn()
        except Exception:
            if attempt == retries - 1:
                raise
            await asyncio.sleep(delay)
