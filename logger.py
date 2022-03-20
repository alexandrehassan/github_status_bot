from datetime import datetime

LOG_LEVEL = "INFO"


def log(level: str, message: str) -> None:
    if level == LOG_LEVEL:
        timeStamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timeStamp} - [{level}] - {message}")
