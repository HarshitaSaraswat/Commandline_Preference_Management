import os
from pathlib import Path

WORKING_DIR = Path(__file__).parent
os.chdir(WORKING_DIR)

def cli():
    import runner

if __name__=="__main__":
    cli()