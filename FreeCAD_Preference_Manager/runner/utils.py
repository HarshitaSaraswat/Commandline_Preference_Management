from pathlib import Path
from typing import List

START_FLAG = "STARTING_044d602c-bcfc-4f4b-96a6-1a1edc357ff2"
EXIT_FLAG = "EXITING_6c6b1739-f167-4415-b2e1-6812875bbbe7"
ERROR_FLAG = "ERROR_e7c5c3a7-e040-49f5-87ef-7c12f3df8538"

SHARE_FILE = Path("share")

def share_args(args: List[str]):
    with SHARE_FILE.open("w") as f:
        f.write(" ".join(args))

def retrive_args():
    args = []
    with SHARE_FILE.open('r') as f:
        args = f.readline().split()
    
    return args