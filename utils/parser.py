import sys
import os



def Error_exit(comment):
    print(f"ERROR: {comment}")
    sys.exit(1)


def check_arg_num(length: int):
    if len(sys.argv) < length:
        Error_exit("Too Few Args")
    elif len(sys.argv) > length:
        Error_exit("Too many Args")


def check_path(path: str):
    if not os.path.exists(path):
        Error_exit(f"{path} doesn't exist")
    elif not os.access(path, os.R_OK):
        Error_exit("Permission Denied")
    return path
