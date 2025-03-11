

import platform

system = platform.system().lower()

if system == "windows":
    import asyncio
    asyncio.set_event_loop_policy(
        asyncio.WindowsProactorEventLoopPolicy()
    )
