import sys
from pathlib import Path

sys.path.append(r"C:\Program Files\FreeCAD 0.21\bin")
WORKING_DIR = Path(__file__).parent.parent
sys.path.append(str(WORKING_DIR))

from src.freecadpm import cli