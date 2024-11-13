from utils import error as er
import sys
import os

def check_arg_num(adjust: int):
	if len(sys.argv) < adjust:
		er.Error_exit("Too Few Args")
	elif len(sys.argv) > adjust:
		er.Error_exit("Too Many Args")

def check_path_ok(path: str):
    if not os.path.exists(path):
        er.Error_exit(f"{path} doesn't exist")
    elif not os.access(path, os.R_OK):
        er.Error_exit("Permission denied")
    return path
