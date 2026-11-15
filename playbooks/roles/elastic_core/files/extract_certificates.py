#!/usr/bin/python3
"""Extract fixed certutil PEM members; see ../../../../docs/elastic-core.md#supporting-tools."""
import json
import os
from pathlib import Path
import sys
import zipfile

kind = sys.argv[1]
if kind not in ("ca", "backend"):
    raise SystemExit("Expected ca or backend")
base = Path("/etc/elastic-demo/pki")
stem = "ca/ca" if kind == "ca" else "elastic-demo/elastic-demo"
changed = False
with zipfile.ZipFile(base / (kind + ".zip")) as archive:
    for suffix in (".crt", ".key"):
        member = stem + suffix
        data = archive.read(member)
        destination = base / member
        destination.parent.mkdir(mode=0o700, exist_ok=True)
        if destination.is_symlink():
            raise SystemExit("Refuse a symbolic certificate destination")
        if destination.exists():
            if destination.read_bytes() != data:
                raise SystemExit("Refuse replacement of existing certificate material")
        else:
            descriptor = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(data)
            changed = True
print(json.dumps({"changed": changed}))
