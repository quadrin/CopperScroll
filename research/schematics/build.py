"""Rebuild every entry schematic from its script.

Usage (from anywhere): python3 -I research/schematics/build.py
Each script in entries/ writes its SVG next to this file. Scripts are deterministic,
so a rebuild with unchanged scripts leaves the SVGs byte-identical.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
scripts = sorted((HERE / "entries").glob("entry_*.py"))
failed = []
for script in scripts:
    result = subprocess.run([sys.executable, "-I", str(script)], capture_output=True, text=True)
    if result.returncode != 0:
        failed.append(script.name)
        print(f"FAILED {script.name}\n{result.stderr}", file=sys.stderr)
print(f"Built {len(scripts) - len(failed)} of {len(scripts)} schematics.")
sys.exit(1 if failed else 0)
