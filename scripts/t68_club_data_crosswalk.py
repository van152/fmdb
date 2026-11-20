#!/usr/bin/env python3
"""Build the t68 Club table_3 data-side L2 crosswalk."""
from __future__ import annotations

import argparse
from bisect import bisect_left, bisect_right
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path, PurePosixPath
from struct import pack, unpack_from
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "scratch/t68/out"
DATA = Path(os.environ.get("FM24_DB_DIR") or (ROOT / "scratch/data")).resolve()
T57 = ROOT / "scratch/t57/out/field_slots.json"
T57_MAP = ROOT / "scratch/t57/out/field_map.json"
N = 84259
HEADER = 13
FOOTER = bytes.fromhex("0000000001e3c03a77")
TAD = bytes.fromhex("03017461642ef10d")
ZSTD_MAGIC = bytes.fromhex("28b52ffd")
CAP = 1_000_000
SIDES = ("client", "server")


class BuildError(RuntimeError):
    pass


def require(ok: Any, message: Any) -> None:
    if not ok:
        raise BuildError(str(message))


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


def u32(data: bytes, at: int = 0) -> int:
    return unpack_from("<I", data, at)[0]


def histogram(values: list[int] | Counter[int]) -> dict[str, int]:
    counter = values if isinstance(values, Counter) else Counter(values)
    return {str(k): counter[k] for k in sorted(counter)}


def dump_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="ascii")


def read_json(path: Path) -> Any:
    require(path.is_file(), f"missing {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def zstd_module():
    try:
        import zstandard  # type: ignore
    except ImportError:
        sys.path.insert(0, str(ROOT.parent / "fm24" / "tools" / "python"))
        import zstandard  # type: ignore
    return zstandard


def archive_entries(blob: bytes, zstd) -> tuple[int, dict[str, tuple[int, int, int]]]:
    """Decode the FMF directory without importing an archive builder."""
    require(len(blob) >= 34 and blob[8:17] == bytes.fromhex("0201666d662e080000"), "FMF shell")
    toc_rel, base_rel = unpack_from("<QQ", blob, 17)
    toc = toc_rel + 17
    base = base_rel + 17
    require(blob[toc : toc + 9] == blob[8:17], "FMF TOC shell")
    dec = zstd.ZstdDecompressor().decompressobj()
    directory = dec.decompress(blob[toc + 9 :])
    used = len(blob) - (toc + 9) - len(dec.unused_data)
    require(dec.eof and toc + 9 + used == len(blob), "TOC closure")
    pos = 0
    entries: dict[str, tuple[int, int, int]] = {}

    def take(width: int) -> bytes:
        nonlocal pos
        require(pos + width <= len(directory), "short TOC")
        value = directory[pos : pos + width]
        pos += width
        return value

    def number() -> int:
        return u32(take(4))

    def text() -> str:
        return take(number()).decode("utf-8")

    def walk(parent: PurePosixPath, depth: int) -> None:
        require(depth < 40, "TOC recursion")
        folder = parent / text()
        for _ in range(number()):
            name = (folder / (text() + text())).as_posix()
            require(name not in entries and ".." not in PurePosixPath(name).parts, "TOC path")
            offset, span, size, _a, _b = unpack_from("<5Q", take(40))
            entries[name] = (base + offset, span, size)
        for _ in range(number()):
            walk(folder, depth + 1)

    walk(PurePosixPath(), 0)
    require(pos == len(directory), "TOC trailing bytes")
    return base, entries


def load_table3(zstd, side: str) -> tuple[bytes, dict[str, Any]]:
    path = DATA / f"{side}_db.dat"
    require(path.is_file(), f"missing archive {path}")
    blob = path.read_bytes()
    base, entries = archive_entries(blob, zstd)
    member = f"{side}_db/table_3.dat"
    require(member in entries, member)
    start, packed_size, declared_size = entries[member]
    end = start + packed_size
    toc = unpack_from("<QQ", blob, 17)[0] + 17
    bound = min((at for at, _span, _size in entries.values() if at > start), default=toc)
    require(base <= start < end <= bound <= len(blob), "member bounds")
    packed = blob[start:end]
    pos = start
    frames: list[list[int]] = []
    candidates: list[bytes] = []
    while pos < end:
        require(blob[pos : pos + 4] == ZSTD_MAGIC, f"zstd magic @{pos}")
        dec = zstd.ZstdDecompressor().decompressobj()
        payload = dec.decompress(blob[pos:end])
        used = end - pos - len(dec.unused_data)
        require(dec.eof and used > 0, "zstd frame")
        frames.append([pos, pos + used, len(payload)])
        if len(payload) == declared_size:
            candidates.append(payload)
        pos += used
    require(pos == end and len(candidates) == 1, "unique declared frame")
    payload = candidates[0]
    require(payload[:8] == TAD and u32(payload, 8) == N, f"table_3 shell/count {side}")
    return payload, {
        "archive": path.as_posix(),
        "archive_sha256": digest(blob),
        "member": member,
        "data_base": base,
        "range": [start, end],
        "bound": bound,
        "declared_size": declared_size,
        "frames": frames,
        "packed_sha256": digest(packed),
        "payload_sha256": digest(payload),
        "count": u32(payload, 8),
    }


def scan_triples(payload: bytes) -> list[list[tuple[int, int]]]:
    """Scan all four alignments for ordinal|UID|UID candidates."""
    try:
        import numpy as np  # type: ignore
    except ImportError:
        points: list[tuple[int, int, int]] = []
        for align in range(4):
            at = align
            while at + 12 <= len(payload):
                ordinal, uid, repeat = unpack_from("<III", payload, at)
                if ordinal < N and uid == repeat:
                    points.append((ordinal, at, uid))
                at += 4
    else:
        points = []
        for align in range(4):
            values = np.frombuffer(payload, dtype="<u4", offset=align, count=(len(payload) - align) // 4)
            hits = np.flatnonzero((values[:-2] < N) & (values[1:-1] == values[2:]))
            points.extend((int(values[i]), 4 * int(i) + align, int(values[i + 1])) for i in hits)
    groups: list[list[tuple[int, int]]] = [[] for _ in range(N)]
    for ordinal, at, uid in sorted(points):
        groups[ordinal].append((at, uid))
    return groups


def scan_pairs(payload: bytes) -> list[list[tuple[int, int]]]:
    """Scan 8-byte ordinal|UID candidates without requiring a repeated UID lane."""
    try:
        import numpy as np  # type: ignore
    except ImportError:
        points: list[tuple[int, int, int]] = []
        for align in range(4):
            at = align
            while at + 8 <= len(payload):
                ordinal, uid = unpack_from("<II", payload, at)
                if ordinal < N:
                    points.append((ordinal, at, uid))
                at += 4
    else:
        points = []
        for align in range(4):
            values = np.frombuffer(payload, dtype="<u4", offset=align, count=(len(payload) - align) // 4)
            hits = np.flatnonzero(values[:-1] < N)
            points.extend((int(values[i]), 4 * int(i) + align, int(values[i + 1])) for i in hits)
    groups: list[list[tuple[int, int]]] = [[] for _ in range(N)]
    for ordinal, at, uid in sorted(points):
        groups[ordinal].append((at, uid))
    return groups


def alignment_counts(groups: list[list[tuple[int, int]]], payload: bytes, triple: bool) -> dict[str, int]:
    counts = [0, 0, 0, 0]
    width = 12 if triple else 8
    for align in range(4):
        at = align
        while at + width <= len(payload):
            ordinal = u32(payload, at)
            if ordinal < N:
                if not triple or u32(payload, at + 4) == u32(payload, at + 8):
                    counts[align] += 1
            at += 4
    require(sum(counts) == sum(map(len, groups)), "candidate alignment count")
    return {str(i): value for i, value in enumerate(counts)}


class Fenwick:
    def __init__(self, size: int):
        self.values = [0] * (size + 1)
        self.last = [-1] * (size + 1)

    def add(self, index: int, value: int, witness: int) -> None:
        index += 1
        while index < len(self.values):
            self.values[index] = min(CAP, self.values[index] + value)
            if value:
                self.last[index] = witness
            index += index & -index

    def query(self, index: int) -> tuple[int, int]:
        total = 0
        witness = -1
        index += 1
        while index > 0:
            total = min(CAP, total + self.values[index])
            witness = max(witness, self.last[index])
            index -= index & -index
        return total, witness


def dp_paths(
    payload: bytes,
    groups: list[list[tuple[int, int]]],
    header: int,
    footer: int,
    width: int,
    markers: set[int] | None,
    nonzero: bool,
    increasing: bool,
    recover: bool = False,
    layers: bool = False,
) -> tuple[dict[str, Any], list[int] | None, dict[str, list[int]] | None]:
    """Count every non-overlapping ordinal-layer tiling, with a safe cap."""
    limit = len(payload) - footer
    previous: list[tuple[int, int, int]] = []
    links: list[dict[int, int | None]] = []
    layer_data = {key: [] for key in ("candidate_counts", "eligible_counts", "state_counts", "partial_path_mass")} if layers else None
    first_dead: int | None = None
    first_rejected: list[int] | None = None

    for ordinal, group in enumerate(groups):
        eligible: list[tuple[int, int]] = []
        for at, uid in group:
            if at < header or at + width > limit:
                continue
            if markers is not None and (at + 12 >= len(payload) or payload[at + 12] not in markers):
                continue
            if nonzero and uid == 0:
                continue
            eligible.append((at, uid))

        current: list[tuple[int, int, int]] = []
        back: dict[int, int | None] = {}
        if ordinal == 0:
            for at, uid in eligible:
                current.append((at, uid, 1))
                if recover:
                    back[at] = None
        elif not increasing:
            prefix: list[int] = [0]
            prefix_last: list[int] = [-1]
            for at, _uid, ways in previous:
                prefix.append(min(CAP, prefix[-1] + ways))
                prefix_last.append(at if ways else prefix_last[-1])
            previous_at = [item[0] for item in previous]
            for at, uid in eligible:
                index = bisect_right(previous_at, at - width)
                ways = prefix[index]
                if ways:
                    current.append((at, uid, ways))
                    if recover:
                        back[at] = prefix_last[index]
        else:
            coords = sorted({uid for _at, uid, _ways in previous})
            positions = {uid: i for i, uid in enumerate(coords)}
            fenwick = Fenwick(len(coords))
            previous_index = 0
            for at, uid in eligible:
                while previous_index < len(previous) and previous[previous_index][0] + width <= at:
                    p_at, p_uid, p_ways = previous[previous_index]
                    fenwick.add(positions[p_uid], p_ways, p_at)
                    previous_index += 1
                uid_index = bisect_left(coords, uid) - 1
                ways, witness = fenwick.query(uid_index) if uid_index >= 0 else (0, -1)
                if ways:
                    current.append((at, uid, ways))
                    if recover:
                        back[at] = witness if witness >= 0 else None

        if layer_data is not None:
            layer_data["candidate_counts"].append(len(group))
            layer_data["eligible_counts"].append(len(eligible))
            layer_data["state_counts"].append(len(current))
            layer_data["partial_path_mass"].append(min(CAP, sum(item[2] for item in current)))
        if not current:
            first_dead = ordinal
            first_rejected = list(group[0]) if group else None
            return {
                "paths": 0,
                "saturated": False,
                "first_dead_ordinal": first_dead,
                "first_rejected_candidate": first_rejected,
                "processed_ordinals": ordinal + 1,
            }, None, layer_data
        previous = current
        if recover:
            links.append(back)

    final = [item for item in previous if item[0] + width == limit]
    total = min(CAP, sum(item[2] for item in final))
    result = {
        "paths": total,
        "saturated": total == CAP,
        "first_dead_ordinal": first_dead,
        "first_rejected_candidate": first_rejected,
        "processed_ordinals": len(groups),
        "terminal_candidates": len(final),
    }
    if not recover or total != 1:
        return result, None, layer_data
    chosen = final[0][0]
    path = [chosen]
    for back in reversed(links[1:]):
        chosen = back[chosen]
        require(chosen is not None, "DP predecessor")
        path.append(chosen)
    path.reverse()
    return result, path, layer_data


def layer_summary(layers: dict[str, list[int]]) -> dict[str, Any]:
    blob = b"".join(pack("<I", value) for key in layers for value in layers[key])
    state = layers["state_counts"]
    mass = layers["partial_path_mass"]
    return {
        "count": len(state),
        "arrays": layers,
        "sha256": digest(blob),
        "single_state_layers": sum(value == 1 for value in state),
        "ambiguous_state_layers": sum(value > 1 for value in state),
        "single_partial_path_layers": sum(value == 1 for value in mass),
        "ambiguous_partial_path_layers": sum(value > 1 for value in mass),
        "max_state_count": max(state),
        "max_partial_path_mass": max(mass),
    }


def sensitivity_for_side(payload: bytes, triple_groups: list[list[tuple[int, int]]], pair_groups: list[list[tuple[int, int]]]) -> tuple[dict[str, Any], list[int], dict[str, Any]]:
    options: dict[str, tuple[list[list[tuple[int, int]]], int, int, int, set[int] | None, bool, bool, bool]] = {}
    for footer in (7, 8, 9, 10, 12):
        options[f"identity_12_footer_{footer}"] = (triple_groups, HEADER, footer, 12, None, True, True, False)
        options[f"identity_13_footer_{footer}_marker0"] = (triple_groups, HEADER, footer, 13, {0}, True, True, False)
        options[f"identity_13_footer_{footer}_no_marker"] = (triple_groups, HEADER, footer, 13, None, True, True, False)
        options[f"identity_8_footer_{footer}"] = (pair_groups, HEADER, footer, 8, None, True, True, False)
    for header in range(11, 16):
        options[f"header_{header}"] = (triple_groups, header, 8, 13, {0, 12}, True, True, False)
    options.update({
        "selector_lookahead_13_footer_8": (triple_groups, HEADER, 8, 13, {0, 12}, True, True, False),
        "triple_12_lookahead_footer_9": (triple_groups, HEADER, 9, 12, {0, 12}, True, True, False),
        "no_marker_12_footer_9": (triple_groups, HEADER, 9, 12, None, True, True, False),
        "allow_zero_12_footer_9": (triple_groups, HEADER, 9, 12, {0, 12}, False, True, False),
        "no_uid_order_12_footer_9": (triple_groups, HEADER, 9, 12, {0, 12}, True, False, False),
        "both_relaxed_12_footer_9": (triple_groups, HEADER, 9, 12, {0, 12}, False, False, False),
    })
    result: dict[str, Any] = {}
    selected: list[int] | None = None
    native_layers: dict[str, Any] | None = None
    for name, (groups, header, footer, width, markers, nonzero, increasing, _unused) in options.items():
        recover = name == "no_marker_12_footer_9"
        check, path, layers = dp_paths(payload, groups, header, footer, width, markers, nonzero, increasing, recover=recover, layers=recover)
        result[name] = check
        if recover:
            require(check["paths"] == 1 and path is not None and layers is not None, "native DP must be unique")
            selected = path
            native_layers = layer_summary(layers)
    require(selected is not None and native_layers is not None, "native selected path")
    return result, selected, native_layers


# The 34 logical positions are copied as data-side grammar labels from t57.
SLOT_KEYS = [
    "selector", "derived_170", "derived_178", "ref_d8", "ref_e0", "ref_e8", "ref_f0", "ref_f8",
    "flags160", "name_len", "name_bytes", "short_len", "short_bytes", "raw16a", "raw166", "person148",
    "raw16c", "vec110", "obj150_tag", "obj150", "vec130", "vec138", "raw168", "stad140", "base_ba",
    "base_b8", "base18", "base30", "base60", "base78", "base90", "base48", "basea8", "identity",
]
SLOT_INDEX = {key: i for i, key in enumerate(SLOT_KEYS)}

PRE = [
    ("selector", 1), ("derived_170", 4), ("derived_178", 1), ("ref_d8", 4), ("ref_e0", 4),
    ("ref_e8", 4), ("ref_f0", 4), ("ref_f8", 4), ("flags160", 6), ("name_len", 4),
    ("name_bytes", None), ("short_len", 4), ("short_bytes", None),
]
EXT = [("raw16a", 1), ("raw166", 2), ("person148", 4), ("raw16c", 1), ("vec110", 1),
       ("obj150_tag", 1), ("obj150", 45), ("vec130", 1), ("vec138", 1), ("raw168", 2), ("stad140", 4)]
BC = [("base18", 1), ("base30", 1), ("base60", 1), ("base78", 1), ("base90", 1), ("base48", 1), ("basea8", 2)]
COL_WIDTH = {"vec110": 4, "vec130": 24, "vec138": 12, "base18": 4, "base30": 4,
             "base60": 4, "base78": 4, "base90": 4, "base48": 16, "basea8": 28}


class Cursor:
    def __init__(self, payload: bytes, limit: int):
        self.payload = payload
        self.p = HEADER
        self.limit = limit
        self.sequence: list[str] = []
        self.book: dict[str, list[tuple[int, int, int]]] = {key: [] for key in SLOT_KEYS}

    def cut(self, row: int, key: str, width: int, extra: int = 0) -> int:
        at = self.p
        self.p += width + extra
        require(0 <= width and self.p <= self.limit, f"row {row} {key} short span @{at}")
        self.sequence.append(key)
        return at

    def record(self, row: int, key: str, width: int, extra: int = 0) -> int:
        at = self.cut(row, key, width, extra)
        self.book[key].append((row, at, width + extra))
        return at

    def number(self, at: int, width: int, signed: bool = False) -> int:
        return int.from_bytes(self.payload[at : at + width], "little", signed=signed)


def replay(payload: bytes, side: str, selected: list[int]) -> dict[str, Any]:
    limit = len(payload) - len(FOOTER)
    cursor = Cursor(payload, limit)
    rows: list[dict[str, int]] = []
    templates: Counter[tuple[int, ...]] = Counter()
    template_rows: dict[tuple[int, ...], list[int]] = {}
    row_templates: list[tuple[int, ...]] = []
    selectors: list[int] = []
    server = side == "server"

    for row in range(N):
        start = cursor.p
        sequence_start = len(cursor.sequence)
        for key, width in PRE[:1]:
            at = cursor.record(row, key, width)
            value = payload[at]
            require(value in (0, 12), f"row {row}: selector {value}")
            selectors.append(value)
            if value == 12:
                for derived, derived_width in PRE[1:3]:
                    cursor.record(row, derived, derived_width)
        for key, width in PRE[3:9]:
            cursor.record(row, key, width)
        for key in ("name", "short"):
            length_key = f"{key}_len"
            at = cursor.record(row, length_key, 4)
            length = u32(payload, at)
            require(length <= limit - cursor.p, f"row {row}: {key} length")
            if length:
                cursor.record(row, f"{key}_bytes", length)

        if server:
            for key, width in EXT[:4]:
                cursor.record(row, key, width)
            at = cursor.record(row, "vec110", 1)
            count = payload[at]
            cursor.book["vec110"][-1] = (row, at, 1 + count * COL_WIDTH["vec110"])
            cursor.p += count * COL_WIDTH["vec110"]
            require(cursor.p <= limit, f"row {row}: vec110")
            at = cursor.record(row, "obj150_tag", 1)
            tag = payload[at]
            if tag == 0:
                cursor.record(row, "obj150", 45)
            else:
                require(tag == 2, f"row {row}: unobserved obj150 tag {tag}")
            for key, width in EXT[7:9]:
                at = cursor.record(row, key, 1)
                count = payload[at]
                cursor.book[key][-1] = (row, at, 1 + count * COL_WIDTH[key])
                cursor.p += count * COL_WIDTH[key]
                require(cursor.p <= limit, f"row {row}: {key}")
            for key, width in EXT[9:]:
                cursor.record(row, key, width)
            cursor.record(row, "base_ba", 1)
            cursor.record(row, "base_b8", 2)
            for key, width in BC:
                at = cursor.record(row, key, width)
                signed = key in {"base60", "base78"}
                count = int.from_bytes(payload[at : at + width], "little", signed=signed)
                require(count >= 0, f"row {row}: {key} negative count {count}")
                cursor.book[key][-1] = (row, at, width + count * COL_WIDTH[key])
                cursor.p += count * COL_WIDTH[key]
                require(cursor.p <= limit, f"row {row}: {key}")
        else:
            # Client has only the two fixed base prefix fields in this grammar.
            cursor.record(row, "base_ba", 1)
            cursor.record(row, "base_b8", 2)

        at = cursor.record(row, "identity", 12)
        require(at == selected[row], f"row {row}: replay identity @{at} != DP @{selected[row]}")
        ordinal, uid, repeat = unpack_from("<III", payload, at)
        require(ordinal == row and uid == repeat and uid != 0, f"row {row}: identity {(ordinal, uid, repeat)}")
        rows.append({"ordinal": row, "start": start, "identity": at, "end": cursor.p, "width": cursor.p - start, "uid": uid})
        sequence = cursor.sequence[sequence_start:]
        template = tuple(SLOT_INDEX[key] for key in sequence)
        templates[template] += 1
        template_rows.setdefault(template, []).append(row)
        row_templates.append(template)

    require(cursor.p == limit and payload[cursor.p:] == FOOTER, f"{side}: footer @{cursor.p}")
    return {
        "rows": rows,
        "book": cursor.book,
        "selectors": selectors,
        "templates": templates,
        "template_rows": template_rows,
        "row_templates": row_templates,
    }


def template_records(templates: Counter[tuple[int, ...]], template_rows: dict[tuple[int, ...], list[int]], reference: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records = []
    for index, item in enumerate(reference):
        execution_order = item["execution_order"]
        sequence = tuple(execution_order)
        rows = templates.get(sequence, 0)
        observed_rows = template_rows.get(sequence, [])
        records.append({
            "reference_index": index,
            "rows": rows,
            "reference_rows": item["rows"],
            "first_ordinal": observed_rows[0] if observed_rows else None,
            "last_ordinal": observed_rows[-1] if observed_rows else None,
            "execution_order": list(execution_order),
            "matches_reference": rows == item["rows"],
        })
    require(set(templates) == {tuple(item["execution_order"]) for item in reference}, "unexpected execution template")
    return records


def coordinate_digest(book: dict[str, list[tuple[int, int, int]]], key: str) -> str:
    return digest(b"".join(pack("<III", row, at, width) for row, at, width in book[key]))


def fixture_witness(replays: dict[str, dict[str, Any]], uids: dict[str, list[int]], t57_map: dict[str, Any]) -> dict[str, Any]:
    regression = t57_map["regression"]
    liverpool: dict[str, Any] = {"ordinal": 460, "uid": {}, "short_name": {}, "nation_ordinal": {}, "city_ordinal": {}}
    for side in SIDES:
        book = replays[side]["book"]
        payload = replays[side]["payload"]
        uid = uids[side][460]
        short_at, short_width = next((at, width) for row, at, width in book["short_bytes"] if row == 460)
        short = payload[short_at : short_at + short_width].decode("utf-8")
        nation_at = book["ref_d8"][460][1]
        city_at = book["ref_f8"][460][1]
        liverpool["uid"][side] = uid
        liverpool["short_name"][side] = short
        liverpool["nation_ordinal"][side] = u32(payload, nation_at)
        liverpool["city_ordinal"][side] = u32(payload, city_at)
        require(uid == 676 and short == "Liverpool" and u32(payload, nation_at) == 139 and u32(payload, city_at) == 1061,
                f"{side}: Liverpool fixture")

    stadium = regression["stadium"]["430"]
    founded = regression["founded_year_fixture_only"]
    liverpool_year = next(item for item in founded if item["row"] == 460)
    require(liverpool_year["year"] == 1892 and liverpool_year["external_year"] == 1892, "Liverpool founded-year witness")
    return {
        "liverpool": liverpool,
        "bernabeu": {
            "source": "scratch/t57/out/field_map.json regression.stadium[430]",
            "stadium_ordinal": 430,
            "uid": 1056,
            "capacity": stadium["capacity_and_seats"][0],
            "seating_capacity": stadium["capacity_and_seats"][1],
            "city_ordinal": stadium["city_ordinal"],
            "rechecked_values": [stadium["uid"], stadium["capacity_and_seats"], stadium["city_ordinal"]],
            "read_by_t68": False,
            "note": "Frozen t57 witness only; t68 scope does not reopen table_21.",
        },
        "founded_year": {
            "source": "scratch/t57/out/field_map.json regression.founded_year_fixture_only",
            "liverpool": {"club_ordinal": 460, "year": 1892, "external_year": 1892},
            "witness_count": len(founded),
            "witness_rows": founded,
            "read_by_t68": False,
            "note": "Frozen t57 witness only; t68 scope does not reopen table_extra_3.",
        },
    }


def build() -> int:
    t57 = read_json(T57)
    t57_map = read_json(T57_MAP)
    zstd = zstd_module()
    payloads: dict[str, bytes] = {}
    archives: dict[str, Any] = {}
    triples: dict[str, list[list[tuple[int, int]]]] = {}
    pairs: dict[str, list[list[tuple[int, int]]]] = {}
    sensitivity: dict[str, Any] = {}
    selected: dict[str, list[int]] = {}
    layers: dict[str, dict[str, Any]] = {}
    replays: dict[str, dict[str, Any]] = {}

    for side in SIDES:
        payloads[side], archives[side] = load_table3(zstd, side)
        triples[side] = scan_triples(payloads[side])
        pairs[side] = scan_pairs(payloads[side])
        sensitivity[side], selected[side], layers[side] = sensitivity_for_side(payloads[side], triples[side], pairs[side])
        require(sensitivity[side]["no_marker_12_footer_9"]["paths"] == 1, f"{side}: native DP")
        replay_data = replay(payloads[side], side, selected[side])
        replay_data["payload"] = payloads[side]
        replays[side] = replay_data

    client_rows = replays["client"]["rows"]
    server_rows = replays["server"]["rows"]
    require([row["uid"] for row in client_rows] == [row["uid"] for row in server_rows], "dual archive UID sequence differs")
    require([row["ordinal"] for row in client_rows] == list(range(N)), "ordinal sequence")
    client_widths = [row["width"] for row in client_rows]
    server_widths = [row["width"] for row in server_rows]
    row_deltas = [server - client for client, server in zip(client_widths, server_widths, strict=True)]
    row_width_crosscheck = {
        "client_row_bytes": sum(client_widths),
        "server_row_bytes": sum(server_widths),
        "client_width_min_max": [min(client_widths), max(client_widths)],
        "server_width_min_max": [min(server_widths), max(server_widths)],
        "server_minus_client": {
            "rows": N,
            "all_positive": all(delta > 0 for delta in row_deltas),
            "min": min(row_deltas),
            "max": max(row_deltas),
        },
    }
    require(
        row_width_crosscheck["client_row_bytes"] == 6_932_060
        and row_width_crosscheck["server_row_bytes"] == 16_595_290
        and row_width_crosscheck["client_width_min_max"] == [54, 156]
        and row_width_crosscheck["server_width_min_max"] == [81, 2618]
        and row_width_crosscheck["server_minus_client"] == {"rows": N, "all_positive": True, "min": 26, "max": 2547},
        "t57 paired row-width cross-check",
    )
    require(payloads["client"][selected["client"][0] : selected["client"][0] + 12] == payloads["server"][selected["server"][0] : selected["server"][0] + 12], "first identity")
    identity_bytes_equal = all(payloads["client"][at : at + 12] == payloads["server"][at2 : at2 + 12] for at, at2 in zip(selected["client"], selected["server"], strict=True))
    require(identity_bytes_equal and payloads["client"][-9:] == FOOTER and payloads["server"][-9:] == FOOTER, "identity/footer equality")

    uids = {side: [row["uid"] for row in replays[side]["rows"]] for side in SIDES}
    templates: dict[str, Any] = {}
    selector_data: dict[str, Any] = {}
    for side in SIDES:
        reference = t57["execution_templates"][side]
        records = template_records(replays[side]["templates"], replays[side]["template_rows"], reference)
        require(all(item["matches_reference"] for item in records), f"{side}: t57 template mismatch")
        templates[side] = records
        selectors = replays[side]["selectors"]
        by_order = {tuple(item["execution_order"]): index for index, item in enumerate(reference)}
        template_indices = [by_order[template] for template in replays[side]["row_templates"]]
        selector_data[side] = {
            "histogram": histogram(selectors),
            "sequence_hex": bytes(selectors).hex(),
            "sequence_sha256": digest(bytes(selectors)),
            "template_index_sequence": template_indices,
            "template_index_sha256": digest(bytes(template_indices)),
            "nonzero_rows": [index for index, value in enumerate(selectors) if value],
            "reference_execution_templates_sha256": digest(T57.read_bytes()),
        }

    fixtures = fixture_witness(replays, uids, t57_map)
    native: dict[str, Any] = {}
    for side in SIDES:
        payload = payloads[side]
        rows = replays[side]["rows"]
        native[side] = {
            "paths": sensitivity[side]["no_marker_12_footer_9"]["paths"],
            "header": HEADER,
            "identity_width": 12,
            "footer": 9,
            "positions": selected[side],
            "positions_sha256": digest(b"".join(pack("<I", at) for at in selected[side])),
            "identity_bytes_sha256": digest(b"".join(payload[at : at + 12] for at in selected[side])),
            "uid_sha256": digest(b"".join(pack("<I", uid) for uid in uids[side])),
            "row_trace_sha256": digest(b"".join(pack("<III", row["start"], row["end"], row["uid"]) for row in rows)),
            "first": [0, selected[side][0], uids[side][0]],
            "last": [N - 1, selected[side][-1], uids[side][-1]],
            "row_width": [min(row["width"] for row in rows), max(row["width"] for row in rows)],
            "row_bytes": sum(row["width"] for row in rows),
            "footer_hex": payload[-9:].hex(),
        }

    crosswalk = {
        "task": "t68",
        "table": 3,
        "entity": "club",
        "grade_target": "L2",
        "status": "complete_data_side_crosswalk",
        "scope": {
            "only_table_3": True,
            "rows_per_side": N,
            "reads_table_21": False,
            "reads_table_extra_3": False,
            "reads_club_link": False,
            "reads_editor_or_ida": False,
            "network": False,
            "z_drive": False,
        },
        "source": {
            "t57_field_slots": T57.as_posix(),
            "t57_field_slots_sha256": digest(T57.read_bytes()),
            "t57_field_map": T57_MAP.as_posix(),
            "t57_field_map_sha256": digest(T57_MAP.read_bytes()),
            "t57_template_reference": "execution_templates only; all table_3 bytes and DP are re-read by t68",
        },
        "archives": archives,
        "native_identity": native,
        "row_width_crosscheck": row_width_crosscheck,
        "identity_crosswalk": {
            "uid_equal": uids["client"] == uids["server"],
            "identity_bytes_equal": identity_bytes_equal,
            "footer_equal": payloads["client"][-9:] == payloads["server"][-9:],
            "uid_count": N,
            "uid_sha256": {side: native[side]["uid_sha256"] for side in SIDES},
            "identity_sha256": {side: native[side]["identity_bytes_sha256"] for side in SIDES},
            "footer_hex": FOOTER.hex(),
        },
        "selectors": selector_data,
        "execution_templates": templates,
        "t57_execution_template_match": {side: all(item["matches_reference"] for item in templates[side]) for side in SIDES},
        "fixtures": fixtures,
        "claims": [
            {"id": "server_full_nonoverlap_dp", "status": "pass", "grade": "L2", "statement": "84,259 server variable rows close as one full non-overlap ordinal-layer path."},
            {"id": "dual_identity", "status": "pass", "grade": "L2", "statement": "Client and server 12-byte identity lanes are equal row by row and UID order is strict."},
            {"id": "dual_footer", "status": "pass", "grade": "L2", "statement": "Both table_3 payloads end in the same 9-byte footer."},
            {"id": "selector_templates", "status": "pass", "grade": "L2", "statement": "Selector histograms, complete selector sequences, and 34-position execution templates agree with t57."},
            {"id": "liverpool_fixture", "status": "pass", "grade": "L2", "statement": "Liverpool row 460 / UID 676 and its nation/city references reclose in both table_3 archives."},
            {"id": "frozen_t01_witnesses", "status": "pass", "grade": "L2", "statement": "Bernabeu and founded-year witnesses are re-acknowledged from the immutable t57 fixture ledger within the table_3-only boundary."},
        ],
        "evidence_level": {"L1": 1, "L2": 1, "L3": 0, "L4": 0},
    }
    sensitivity_out = {
        "task": "t68",
        "table": 3,
        "method": {
            "full_dp": True,
            "sampled": False,
            "processed_rows_per_side": N,
            "nonoverlap": True,
            "ordinal_layered": True,
            "path_count_cap": CAP,
            "cap_does_not_affect_uniqueness": True,
            "native_rule": "header 13; 12-byte ordinal|UID|UID identity; UID nonzero and strictly increasing; footer 9",
        },
        "candidate_scan": {
            side: {
                "triple_total": sum(map(len, triples[side])),
                "triple_histogram": histogram([len(group) for group in triples[side]]),
                "triple_alignment_counts": alignment_counts(triples[side], payloads[side], True),
                "pair_total": sum(map(len, pairs[side])),
                "pair_histogram": histogram([len(group) for group in pairs[side]]),
                "pair_alignment_counts": alignment_counts(pairs[side], payloads[side], False),
            }
            for side in SIDES
        },
        "sides": sensitivity,
        "native_selected_positions": selected,
        "native_layers": layers,
        "dual_identity": crosswalk["identity_crosswalk"],
        "sensitivity_notes": {
            "identity_13": "13-byte t50-style lookahead is not native; marker-0 controls retain the ordinal 69705 break, while selector-lookahead {0,12} with footer 8 is an alternate closure equivalent to native 12+footer9.",
            "identity_8": "8-byte controls scan ordinal|UID pairs without requiring a repeated UID lane; they are negative controls for the native 12-byte triple.",
            "uid_relaxation": "allow_zero, no_uid_order, and both_relaxed are full DP controls; counts are not sampled.",
        },
    }
    dump_json(OUT / "crosswalk.json", crosswalk)
    dump_json(OUT / "sensitivity.json", sensitivity_out)
    print(f"t68 build PASS: {N} client + {N} server rows; native identity paths=1/1")
    return 0


def selftest() -> int:
    payload = TAD + pack("<I", 2) + b"\0"
    payload += pack("<III", 0, 10, 10) + b"abc"
    payload += pack("<III", 1, 20, 20) + FOOTER
    groups = [[] for _ in range(2)]
    groups[0].append((13, 10))
    groups[1].append((28, 20))
    result, path, _layers = dp_paths(payload, groups, 13, 9, 12, None, True, True, recover=True, layers=True)
    require(result["paths"] == 1 and path == [13, 28], (result, path))
    wrong, _path, _layers = dp_paths(payload, groups, 13, 8, 12, None, True, True)
    require(wrong["paths"] == 0, wrong)
    print("t68 builder selftest PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, epilog="Exit codes: 0 success, 1 check failure, 2 fatal/usage error.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--build", action="store_true", help="decode table_3 and write scratch/t68/out")
    group.add_argument("--selftest", action="store_true", help="run synthetic DP selftests")
    args = parser.parse_args()
    try:
        return selftest() if args.selftest else build()
    except BuildError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f"FATAL: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
