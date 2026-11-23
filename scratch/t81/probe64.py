"""t81-fix1 probe64 — is_client_field flags + exact column sets for injury."""
import json
import runpy
import struct
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
core = runpy.run_path(str(REPO / "scripts" / "t73_mapper_core.py"), run_name="p64")
M = json.loads((REPO / "evidence/fm24/reports/editor_schema/master.json").read_text("utf-8"))

print("--- injury.xml field records (raw keys)")
for f in M["entities"]["injury.xml"][0]["fields"]:
    print("  ", json.dumps(f, ensure_ascii=False))

print("--- field_codes for Imio/Icdo/Iexd/Iiar/Igpr/Ibph")
for c in ("Imio", "Icdo", "Iexd", "Iiar", "Igpr", "Ibph", "Ibsp", "Ibin", "Ibis", "Ibpg"):
    print("  ", c, json.dumps(M["field_codes"].get(c), ensure_ascii=False)[:220])
