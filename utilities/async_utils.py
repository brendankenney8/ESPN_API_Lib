import asyncio


def run(coro):
    """
    Run an async coroutine from synchronous code.

    - If no event loop is running in this thread, uses asyncio.run(coro).
    - If an event loop is already running (e.g., Jupyter), raise a clear error instructing
      the caller to use the async variant of the API instead.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        raise RuntimeError(
            "A running event loop was detected. Use the async API (e.g., await Game.get_async(...)) instead of the sync wrapper."
        )

    return asyncio.run(coro)
