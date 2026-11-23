"""Read-only helpers for independently loading server_db.dat table payloads."""
from __future__ import annotations

import hashlib
import runpy
from functools import lru_cache
from pathlib import Path
from typing import Any

ARCHIVE = Path(r"Z:\SteamLibrary\steamapps\common\Football Manager 2024\data\database\db\2430\2430_fm\server_db.dat")
CENSUS = Path(r"D:\tmp2b\fm24\reports\dbdat_decode\server_tables_census.json")
READER = Path(r"D:\tmp2b\fm24\scripts\modding_read_dbdat.py")
ZSTD_MAGIC = bytes.fromhex("28 b5 2f fd")


@lru_cache(maxsize=2)
def load_environment(archive: str | Path = ARCHIVE) -> tuple[dict[str, Any], bytes, dict[str, Any], list[dict[str, Any]]]:
    """Load the upstream read-only archive helper and the raw archive bytes."""
    helper = runpy.run_path(str(READER))
    path, data, layout = helper["_entries"](archive, archive="server_db.dat")
    entries = helper["list_tables"](archive, archive="server_db.dat")
    return helper, data, layout, entries


def load_payload(table_id: int, archive: str | Path = ARCHIVE) -> tuple[bytes, dict[str, Any]]:
    """Resolve/decompress one member, scanning its first 64 bytes for frame magic.

    Returns (payload, directory_entry). Checks directory size and, when present,
    the independent census size and SHA-256 expectation.
    """
    helper, data, layout, entries = load_environment(archive)
    entry = helper["_resolve_table"](table_id, entries, "server_db.dat")
    member_start = layout["data_base"] + entry["offset"]
    member_end = member_start + entry["packed_size"]
    if not (0 <= member_start < member_end <= len(data)):
        raise ValueError(f"table_{table_id}: directory member is outside archive")
    window = data[member_start : min(member_end, member_start + 64)]
    relative = window.find(ZSTD_MAGIC)
    if relative < 0:
        raise ValueError(f"table_{table_id}: Zstandard magic absent in first 64 member bytes")
    frame_start = member_start + relative
    payload = helper["_stream_decompress"](data[frame_start:member_end], entry["size"])
    if len(payload) != entry["size"]:
        raise AssertionError(f"table_{table_id}: decompressed size {len(payload)} != directory {entry['size']}")
    census = __import__("json").loads(CENSUS.read_text(encoding="utf-8"))
    expected = next((item for item in census["entries"] if item.get("table_id") == table_id), None)
    if expected is None:
        raise AssertionError(f"table_{table_id}: absent from independent census")
    if len(payload) != expected["payload_size"]:
        raise AssertionError(f"table_{table_id}: payload size {len(payload)} != census {expected['payload_size']}")
    digest = hashlib.sha256(payload).hexdigest()
    if expected.get("payload_sha256") is not None and digest != expected["payload_sha256"]:
        raise AssertionError(f"table_{table_id}: payload SHA-256 {digest} != census {expected['payload_sha256']}")
    entry = dict(entry)
    entry.update({"frame_relative_offset": relative, "payload_sha256": digest,
                  "census_sha256": expected.get("payload_sha256"),
                  "census_sha256_present": expected.get("payload_sha256") is not None})
    return payload, entry
