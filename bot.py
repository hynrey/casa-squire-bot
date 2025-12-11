import asyncio
import os

from src.main import main

PID_FILE = "bot.pid"


def cleanup():
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)


if __name__ == "__main__":
    cleanup()

    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    asyncio.run(main())
