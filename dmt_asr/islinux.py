from platform import system

def is_linux() -> bool:
    return system().lower() == "linux"


def check_linux_or_error():
    if not is_linux():
        raise ValueError("NOT LINUX")