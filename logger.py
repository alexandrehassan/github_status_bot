from datetime import datetime


def log(level: str, message: str) -> None:
    timeStamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timeStamp} - [{level}] - {message}")
