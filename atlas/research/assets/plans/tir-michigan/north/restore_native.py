from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent
record = json.loads((root / "manifest.json").read_text())["native_resolution_derivative"]
data = bytearray()
for part in record["parts"]:
    payload = (root / part["filename"]).read_bytes()
    if hashlib.sha256(payload).hexdigest() != part["sha256"]:
        raise SystemExit("Part checksum failed: " + part["filename"])
    data.extend(payload)
if len(data) != record["bytes"] or hashlib.sha256(data).hexdigest() != record["sha256"]:
    raise SystemExit("Native-resolution JPEG checksum failed")
target = root / record["filename"]
if target.exists() and target.read_bytes() != data:
    raise SystemExit("Refusing to overwrite a different file: " + str(target))
target.write_bytes(data)
print(target)
