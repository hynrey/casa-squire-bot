import logging
import subprocess


def schedule_shutdown(seconds: int):
    logging.info(f"Shutting down in {seconds} seconds")
    subprocess.run(["cmd.exe", "/c", f"shutdown /s /t {seconds}"])


def abort_shutdown():
    logging.info("Aborting shutdown")
    subprocess.run(["cmd.exe", "/c", "shutdown /a"], check=True)
