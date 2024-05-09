from datetime import datetime


def print_log(message, level='INFO', delay=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if delay is not None:
        print(f"[{timestamp}] [{level}] {message}. Waiting for {delay} seconds...")
    else:
        print(f"[{timestamp}] [{level}] {message}")
