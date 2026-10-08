#!/usr/bin/env python3
"""Run semantic tests and verify that the reviewed/generated snapshots are current."""
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
for directory in (HERE, *(HERE / name for name in ("relationships", "inventory", "states", "coverage", "decisions"))):
    subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", str(directory), "-p", "test_*.py"], check=True)
subprocess.run([sys.executable, str(HERE / "build.py"), "--check"], check=True)
