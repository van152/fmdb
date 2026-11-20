"""Build the t67 COMP table_25 data-side crosswalk."""
from __future__ import annotations

import argparse
from bisect import bisect_right
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path, PurePosixPath
from struct import pack, unpack_from
import sys
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "scratch/t67/out"
DATA = Path(os.environ.get("FM24_DB_DIR") or (ROOT / "scratch/data")).resolve()
T59 = ROOT / "scratch/t59/out/field_slots.json"
T01F = ROOT / "reports/t01f_comp_row_offsets.json"
N = 7047
HEADER = 13
FOOTER = bytes.fromhex("00000000014ec43a77")
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


def i16(data: bytes, at: int) -> int:
    return unpack_from("<h", data, at)[0]


def histogram(values: list[int] | Counter[int]) -> dict[str, int]:
    counter = values if isinstance(values, Counter) else Counter(values)
    return {str(k): counter[k] for k in sorted(counter)}


def dump_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True, sort_keys=False) + "\n", encoding="ascii")


def zstd_module():
    try:
        import zstandard  # type: ignore
    except ImportError:
        sys.path.insert(0, str(ROOT.parent / "fm24" / "tools" / "python"))
        import zstandard  # type: ignore
    return zstandard


def archive_entries(blob: bytes, zstd) -> tuple[int, dict[str, tuple[int, int, int]]]:
    require(len(blob) >= 34 and blob[8:17] == bytes.fromhex("0201666d662e080000"), "FMF shell")
    toc_rel, base_rel = unpack_from("<QQ", blob, 17)
    toc = toc_rel + 17
    base = base_rel + 17
    require(blob[toc : toc + 9] == blob[8:17], "FMF TOC shell")
    dec = zstd.ZstdDecompressor().decompressobj()
    directory = dec.decompress(blob[toc + 9 :])
    used = len(blob) - (toc + 9) - len(dec.unused_data)
    require(dec.eof and toc + 9 + used == len(blob), "TOC frame closure")
    pos = 0
    entries: dict[str, tuple[int, int, int]] = {}

    def take(width: int) -> bytes:
        nonlocal pos
        require(pos + width <= len(directory), "short TOC")
        out = directory[pos : pos + width]
        pos += width
        return out

    def number() -> int:
        return unpack_from("<I", take(4))[0]

    def text() -> str:
        raw = take(number())
        return raw.decode("utf-8")

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


def load_table25(zstd, side: str) -> tuple[bytes, dict[str, Any]]:
    path = DATA / f"{side}_db.dat"
    require(path.is_file(), f"missing archive {path}")
    blob = path.read_bytes()
    base, entries = archive_entries(blob, zstd)
    member = f"{side}_db/table_25.dat"
    require(member in entries, f"missing {member}")
    start, packed_size, declared_size = entries[member]
    end = start + packed_size
    bound = min((at for at, _span, _size in entries.values() if at > start), default=unpack_from("<QQ", blob, 17)[0] + 17)
    require(base <= start < end <= bound <= len(blob), f"member bounds {member}")
    packed = blob[start:end]
    pos = start
    frames: list[list[int]] = []
    candidates: list[bytes] = []
    while pos < end:
        require(blob[pos : pos + 4] == ZSTD_MAGIC, f"zstd magic @{pos}")
        dec = zstd.ZstdDecompressor().decompressobj()
        payload = dec.decompress(blob[pos:end])
        used = end - pos - len(dec.unused_data)
        require(dec.eof and used > 0, f"zstd frame @{pos}")
        frames.append([pos, pos + used, len(payload)])
        if len(payload) == declared_size:
            candidates.append(payload)
        pos += used
    require(pos == end and len(candidates) == 1, f"unique sized frame {member}")
    payload = candidates[0]
    require(payload[:8] == TAD and u32(payload, 8) == N, f"COMP shell/count {side}")
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


def scan_triples(payload: bytes, count: int) -> list[list[tuple[int, int]]]:
    """Scan all four byte alignments for ordinal|uid|uid triples."""
    groups: list[list[tuple[int, int]]] = [[] for _ in range(count)]
    for align in range(4):
        at = align
        while at + 12 <= len(payload):
            ordinal, uid, repeat = unpack_from("<III", payload, at)
            if ordinal < count and uid == repeat:
                groups[ordinal].append((at, uid))
            at += 4
    for group in groups:
        group.sort()
    return groups


def alignment_counts(payload: bytes, count: int) -> dict[str, int]:
    counts = [0, 0, 0, 0]
    for align in range(4):
        at = align
        while at + 12 <= len(payload):
            ordinal, uid, repeat = unpack_from("<III", payload, at)
            if ordinal < count and uid == repeat:
                counts[align] += 1
            at += 4
    return {str(index): value for index, value in enumerate(counts)}


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
) -> tuple[dict[str, Any], list[int] | None]:
    """Count non-overlapping ordinal-layer tilings, capped for relaxed cases."""
    limit = len(payload) - footer
    previous: list[tuple[int, int, int]] = []
    links: list[dict[int, int | None]] = []
    first_dead: int | None = None
    first_rejected: list[int] | None = None

    for ordinal, group in enumerate(groups):
        current: list[tuple[int, int, int]] = []
        back: dict[int, int | None] = {}
        if not increasing:
            previous_at = [item[0] for item in previous]
            prefix = [0]
            for _at, _uid, ways in previous:
                prefix.append(min(CAP, prefix[-1] + ways))
        for at, uid in group:
            if at < header or at + width > limit:
                continue
            if markers is not None:
                if at + 12 >= len(payload) or payload[at + 12] not in markers:
                    continue
            if nonzero and uid == 0:
                continue
            if ordinal == 0:
                ways = 1
                predecessor = None
            elif not increasing:
                index = bisect_right(previous_at, at - width)
                ways = prefix[index]
                predecessor = previous[index - 1][0] if ways else None
            else:
                ways = 0
                predecessor = None
                for previous_at_one, previous_uid, previous_ways in previous:
                    if previous_at_one + width > at:
                        break
                    if previous_uid < uid:
                        ways = min(CAP, ways + previous_ways)
                        predecessor = previous_at_one
                        if ways >= CAP:
                            break
            if ways:
                current.append((at, uid, min(CAP, ways)))
                if recover:
                    back[at] = predecessor
        if not current:
            first_dead = ordinal
            first_rejected = list(group[0]) if group else None
            result = {
                "paths": 0,
                "saturated": False,
                "first_dead_ordinal": first_dead,
                "first_rejected_candidate": first_rejected,
            }
            return result, None
        previous = current
        if recover:
            links.append(back)

    final = [item for item in previous if item[0] + width == limit]
    total = min(CAP, sum(item[2] for item in final))
    result = {
        "paths": total,
        "saturated": total == CAP,
        "first_dead_ordinal": None,
        "first_rejected_candidate": None,
    }
    if not recover or total != 1:
        return result, None
    chosen = final[0][0]
    path = [chosen]
    for link in reversed(links[1:]):
        chosen = link[chosen]
        require(chosen is not None, "missing unique DP predecessor")
        path.append(chosen)
    path.reverse()
    return result, path


def options() -> dict[str, tuple[int, int, int, set[int] | None, bool, bool]]:
    out: dict[str, tuple[int, int, int, set[int] | None, bool, bool]] = {}
    for footer in (7, 8, 9, 10, 12):
        out[f"identity_12_footer_{footer}"] = (HEADER, footer, 12, None, True, True)
        out[f"marker_0_footer_{footer}"] = (HEADER, footer, 13, {0}, True, True)
        out[f"triple_footer_{footer}"] = (HEADER, footer, 12, {0, 12}, True, True)
    for header in range(11, 16):
        out[f"header_{header}"] = (header, 8, 13, {0, 12}, True, True)
    out.update(
        selector_lookahead=(HEADER, 8, 13, {0, 12}, True, True),
        no_marker=(HEADER, 8, 13, None, True, True),
        allow_zero=(HEADER, 8, 13, {0, 12}, False, True),
        no_uid_order=(HEADER, 8, 13, {0, 12}, True, False),
        both_relaxed=(HEADER, 8, 13, {0, 12}, False, False),
        wire_triple=(HEADER, 9, 12, {0}, True, True),
        triple_no_lookahead=(HEADER, 9, 12, None, True, True),
        native_identity=(HEADER, 9, 12, None, True, True),
    )
    return out


def fixed_client_assumption(payload: bytes, width: int, footer: int, lookahead: bool = False) -> dict[str, Any]:
    row_width = 127
    starts = [HEADER + i * row_width for i in range(N)]
    limit = len(payload) - footer
    positions: list[int] = []
    for ordinal, start in enumerate(starts):
        at = start + row_width - (12 if lookahead else width)
        if at + 12 > len(payload):
            return {"paths": 0, "reason": "triple outside payload", "first_dead_ordinal": ordinal}
        x, uid, repeat = unpack_from("<III", payload, at)
        marker_ok = not lookahead or (at + 12 < len(payload) and payload[at + 12] == 0)
        if x != ordinal or uid != repeat or uid == 0 or not marker_ok:
            return {
                "paths": 0,
                "reason": "row-end identity bytes do not satisfy the assumption",
                "first_dead_ordinal": ordinal,
                "candidate": [at, x, uid, repeat, payload[at + 12] if at + 12 < len(payload) else None],
            }
        if at + (13 if lookahead else width) > limit:
            return {"paths": 0, "reason": "footer closure", "first_dead_ordinal": ordinal}
        positions.append(at)
    closed = positions[-1] + (13 if lookahead else width) == limit
    return {
        "paths": 1 if closed else 0,
        "reason": "closed fixed-width row formula" if closed else "fixed-width footer does not close",
        "first_dead_ordinal": None if closed else N - 1,
        "row_width": row_width,
        "identity_width": 13 if lookahead else width,
        "footer": footer,
        "positions_sha256": digest(b"".join(pack("<I", x) for x in positions)),
    }


class RowBytes:
    def __init__(self, payload: bytes, start: int, identity: int):
        self.payload = payload
        self.p = start
        self.identity = identity
        self.sequence: list[str] = []
        self.events: dict[str, dict[str, Any]] = {}

    def raw(self, width: int) -> bytes:
        require(width >= 0 and self.p + width <= self.identity, f"row short span @{self.p} width {width}")
        raw = self.payload[self.p : self.p + width]
        self.p += width
        return raw

    def event(self, key: str, width: int, signed: bool = False) -> int:
        at = self.p
        if key == "identity":
            require(self.p == self.identity and width == 12, (key, self.p, self.identity, width))
            raw = self.payload[self.p : self.p + width]
            self.p += width
        else:
            raw = self.raw(width)
        value = int.from_bytes(raw, "little", signed=signed)
        self.sequence.append(key)
        self.events[key] = {"at": at, "width": width, "raw": raw.hex(), "value": value}
        return value

    def dynamic(self, key: str, fn: Callable[[], None]) -> None:
        at = self.p
        try:
            fn()
        except BuildError as exc:
            raise BuildError(f"{key} @{at}: {exc}") from exc
        self.sequence.append(key)
        self.events[key] = {
            "at": at,
            "width": self.p - at,
            "raw": self.payload[at : self.p].hex(),
            "value": None,
        }

    def number(self, width: int, signed: bool = False) -> int:
        return int.from_bytes(self.raw(width), "little", signed=signed)


PRE = [
    ("selector", 1), ("m15c", 1), ("m15d", 1), ("colour_tag", 1),
    ("m120", 2), ("m124", 2), ("m128", 2), ("m12c", 2), ("m130", 2),
    ("m134", 1), ("m1a0", 1), ("m1a2", 1), ("m1a3", 1), ("m1a4", 1),
    ("m1a5", 1), ("stat_a_tag", 1), ("m198", 1), ("m199", 1),
    ("m19a", 1), ("m19b", 1), ("m19c", 1), ("m19d", 1), ("m19e", 1),
    ("stat_b_tag", 1), ("m189_197", 15), ("mf6", 1), ("m138", 4),
    ("m13c", 4), ("m58", 4), ("m60", 4), ("m70", 4), ("m68", 4),
    ("m150", 2),
]
EXT0 = [("m180", 2), ("mb8", 4), ("m188", 1), ("m184", 2), ("m186", 2),
        ("m182", 2), ("m160", 8), ("m168", 8), ("m170", 8), ("m178", 8)]
EXT1 = [("mf0", 4), ("m1a1", 1), ("m1a8", 1), ("mf4", 1), ("mf5", 1)]
POST = [("m148", 4), ("m152", 2), ("m154", 2), ("m156", 2), ("m158", 2),
        ("m15a", 2), ("m80", 4), ("m88", 4), ("m90", 4), ("m98", 4)]
POST_TAIL = [("m140", 4), ("m144", 4), ("mf7", 1), ("mf8", 1), ("mf9", 1)]


def parse_row(payload: bytes, start: int, identity: int, server: bool) -> tuple[list[str], dict[str, dict[str, Any]]]:
    row = RowBytes(payload, start, identity)
    for key, width in PRE:
        row.event(key, width)

    if server:
        for key, width in EXT0:
            row.event(key, width)

        def vec30() -> None:
            count = row.number(4)
            require(0 <= count <= identity - row.p, "vec30 count")
            row.raw(2 * count)

        row.dynamic("vec30", vec30)
        a8_present = row.event("a8_present", 1)

        if a8_present:
            def a8() -> None:
                revision = row.number(1)
                row.raw(32 + 4 * (revision >= 2) + 9 + (2 if revision >= 3 else 1) + 4 + 4)
            row.dynamic("obj_a8", a8)

        for key, width in EXT1:
            row.event(key, width)

        e0_present = row.event("e0_present", 1)
        if e0_present:
            def e0() -> None:
                require(row.number(4) == 0, "untraced e0 payload")
            row.dynamic("obj_e0", e0)

        def vec18() -> None:
            count = row.number(4, signed=True)
            require(0 <= count <= identity - row.p, "vec18 count")
            for _ in range(count):
                revision = row.number(1, signed=True)
                row.raw(7 + (revision >= 2))
        row.dynamic("vec18", vec18)

        e8_present = row.event("e8_present", 1)
        if e8_present:
            def e8() -> None:
                row.raw(4)
                count = row.number(4)
                require(0 <= count <= identity - row.p, "e8 count")
                for _ in range(count):
                    revision = row.number(2, signed=True)
                    row.raw(6 + (2 if revision >= 2 else 1) + 1 + (revision >= 3))
            row.dynamic("obj_e8", e8)

        c0_present = row.event("c0_present", 1)
        if c0_present:
            def c0() -> None:
                row.raw(1)
                count = row.number(4)
                require(0 <= count <= identity - row.p, "c0 count")
                for _ in range(count):
                    row.raw(2)
                    inner = row.number(4)
                    require(0 <= inner <= identity - row.p, "c0 inner count")
                    row.raw(12 * inner)
            row.dynamic("obj_c0", c0)

        c8_present = row.event("c8_present", 1)
        if c8_present:
            row.dynamic("obj_c8", lambda: row.raw(25))
        row.event("m1a7", 1)

        d0_present = row.event("d0_present", 1)
        if d0_present:
            row.dynamic("obj_d0", lambda: row.raw(15))
        d8_present = row.event("d8_present", 1)
        if d8_present:
            row.dynamic("obj_d8", lambda: row.raw(15))

        def vec100() -> None:
            count = row.number(2, signed=True)
            require(count >= 0 and count <= identity - row.p, "vec100 count")
            row.raw(5 * count)
        row.dynamic("vec100", vec100)

    for key, width in POST:
        row.event(key, width)
    wbcl_present = row.event("wbcl_present", 1)
    if wbcl_present:
        row.event("m14c", 2)
    for key, width in POST_TAIL:
        row.event(key, width)
    row.event("identity", 12)
    require(row.p == identity + 12, f"row grammar ended @{row.p}, expected {identity + 12}")
    return row.sequence, row.events


def row_layout(payload: bytes, positions: list[int]) -> list[dict[str, int]]:
    limit = len(payload) - len(FOOTER)
    rows: list[dict[str, int]] = []
    for ordinal, identity in enumerate(positions):
        start = HEADER if ordinal == 0 else positions[ordinal - 1] + 12
        end = identity + 12
        require(start <= identity and end <= limit, (ordinal, start, identity, end, limit))
        rows.append({"ordinal": ordinal, "start": start, "identity": identity, "end": end, "width": end - start})
    require(rows and rows[-1]["end"] == limit, "row layout footer closure")
    return rows


def template_records(counter: Counter[tuple[str, ...]], first: dict[tuple[str, ...], int], last: dict[tuple[str, ...], int], reference: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result = []
    for index, item in enumerate(reference):
        sequence = tuple(item["sequence"])
        result.append({
            "reference_index": index,
            "rows": counter.get(sequence, 0),
            "reference_rows": item["rows"],
            "first_ordinal": first.get(sequence),
            "last_ordinal": last.get(sequence),
            "sequence": list(sequence),
            "sequence_sha256": digest(json.dumps(list(sequence), separators=(",", ":")).encode("ascii")),
            "matches_reference": counter.get(sequence, 0) == item["rows"],
        })
    for sequence, count in counter.items():
        if not any(tuple(item["sequence"]) == sequence for item in reference):
            result.append({
                "reference_index": None,
                "rows": count,
                "reference_rows": None,
                "first_ordinal": first[sequence],
                "last_ordinal": last[sequence],
                "sequence": list(sequence),
                "sequence_sha256": digest(json.dumps(list(sequence), separators=(",", ":")).encode("ascii")),
                "matches_reference": False,
            })
    return result


def fixed_events(data: dict[str, Any], key: str, ordinal: int) -> dict[str, Any]:
    event = data["event_values"][key][ordinal]
    require(event is not None, (key, ordinal, "missing event"))
    return event


def fixtures(all_data: dict[str, dict[str, Any]], payloads: dict[str, bytes]) -> dict[str, Any]:
    prior = json.loads(T01F.read_text(encoding="utf-8"))
    named = []
    for item in prior["verification"]["continent_and_nation_named_anchors"]:
        ordinal = item["row_index"]
        result = {"row": ordinal, "name": item["prior_english_name"], "uid": item["dbid"], "sides": {}}
        for side in SIDES:
            data = all_data[side]
            require(data["uids"][ordinal] == item["dbid"], (side, ordinal, "named UID"))
            side_result: dict[str, Any] = {"uid": data["uids"][ordinal], "slots": {}}
            for slot, field in (("m58", "ccti"), ("m60", "cnti")):
                event = fixed_events(data, slot, ordinal)
                expected_raw = bytes.fromhex(item[field]["bytes"].replace(" ", ""))
                require(event["value"] == int.from_bytes(expected_raw, "little"), (side, ordinal, field, event))
                if side == "client":
                    require(event["at"] == int(item[field]["payload_offset"], 16), (side, ordinal, field, "offset"))
                side_result["slots"][field] = {
                    "at": event["at"], "raw": event["raw"], "value": event["value"],
                    "expected_raw": expected_raw.hex(),
                }
            result["sides"][side] = side_result
        named.append(result)

    parents = []
    for item in prior["verification"]["cpcm_named_anchors"]:
        child = item["row_index"]
        parent = item["expected_parent_ordinal"]
        result = {"child_row": child, "parent_ordinal": parent, "parent_uid": item["parent_dbid"], "sides": {}}
        for side in SIDES:
            data = all_data[side]
            require(data["uids"][child] == item["child_dbid"], (side, child, "child UID"))
            require(data["uids"][parent] == item["parent_dbid"], (side, parent, "parent UID"))
            event = fixed_events(data, "m68", child)
            require(event["value"] == parent, (side, child, "parent ordinal"))
            result["sides"][side] = {
                "child_uid": data["uids"][child],
                "parent_uid": data["uids"][parent],
                "at": event["at"],
                "raw": event["raw"],
                "value": event["value"],
            }
        parents.append(result)

    continent_values = {}
    for side in SIDES:
        values = [fixed_events(all_data[side], "m58", i)["value"] for i in range(N)]
        live = sorted({value for value in values if value != 0xFFFFFFFF})
        require(live == list(range(6)), (side, "six continent ordinals", live))
        continent_values[side] = live
    field_map_path = ROOT / "scratch/t59/out/field_map.json"
    field_map_bytes = field_map_path.read_bytes()
    field_map = json.loads(field_map_bytes.decode("utf-8"))
    target_england = field_map["fixtures"]["England"]
    target_china = field_map["fixtures"]["China_PR"]
    england_rows = [7, 664]
    china_rows = [245, 250]
    england_values = {side: [fixed_events(all_data[side], "m60", row)["value"] for row in england_rows] for side in SIDES}
    china_values = {side: [fixed_events(all_data[side], "m60", row)["value"] for row in china_rows] for side in SIDES}
    require(all(values == [target_england[0]] * len(england_rows) for values in england_values.values()), england_values)
    require(all(values == [target_china[0]] * len(china_rows) for values in china_values.values()), china_values)
    return {
        "named_anchors": named,
        "parent_anchors": parents,
        "live_continent_ordinals": continent_values,
        "England": {"nation_ordinal": target_england[0], "nation_uid": {"client": target_england[1], "server": target_england[1]}, "comp_rows": england_rows, "comp_m60_values": england_values},
        "China_PR": {"nation_ordinal": target_china[0], "nation_uid": {"client": target_china[1], "server": target_china[1]}, "comp_rows": china_rows, "comp_m60_values": china_values},
        "negative_parent_ordinals": [],
        "target_fixture_reference": {"path": field_map_path.as_posix(), "sha256": digest(field_map_bytes)},
    }


def process_side(payload: bytes, side: str, reference: dict[str, Any]) -> dict[str, Any]:
    groups = scan_triples(payload, N)
    alignment_candidate_counts = alignment_counts(payload, N)
    sensitivity: dict[str, Any] = {}
    selected: list[int] | None = None
    for name, args in options().items():
        result, path = dp_paths(payload, groups, *args, recover=name in {"native_identity", "wire_triple"})
        sensitivity[name] = result
        if name == "native_identity":
            require(result["paths"] == 1 and path is not None, (side, "native identity unique"))
            selected = path
    require(selected is not None, "native path")
    rows = row_layout(payload, selected)
    uids = [unpack_from("<I", payload, at + 4)[0] for at in selected]
    require([unpack_from("<I", payload, at)[0] for at in selected] == list(range(N)), (side, "ordinals"))
    require(all(unpack_from("<I", payload, at + 8)[0] == uid for at, uid in zip(selected, uids)), (side, "repeated UID"))
    require(all(uid > 0 for uid in uids) and all(a < b for a, b in zip(uids, uids[1:])), (side, "UID order"))
    require(payload[len(payload) - len(FOOTER) :] == FOOTER, (side, "footer"))

    sequence_counter: Counter[tuple[str, ...]] = Counter()
    first: dict[tuple[str, ...], int] = {}
    last: dict[tuple[str, ...], int] = {}
    event_values: dict[str, list[dict[str, Any] | None]] = {key: [None] * N for key in ("m58", "m60", "m68")}
    selector_values: list[int] = []
    marker_counts: dict[str, Counter[int]] = {key: Counter() for key in ("selector", "colour_tag", "stat_a_tag", "stat_b_tag", "wbcl_present")}
    no_inline = 0
    for row in rows:
        try:
            seq, events = parse_row(payload, row["start"], row["identity"], side == "server")
        except BuildError as exc:
            raise BuildError(f"{side} row {row['ordinal']} start={row['start']} identity={row['identity']}: {exc}") from exc
        sequence = tuple(seq)
        sequence_counter[sequence] += 1
        first.setdefault(sequence, row["ordinal"])
        last[sequence] = row["ordinal"]
        for key in event_values:
            if key in events:
                event_values[key][row["ordinal"]] = events[key]
        for key in marker_counts:
            marker_counts[key][events[key]["value"]] += 1
        selector_values.append(events["selector"]["value"])
        if events["m1a0"]["value"] != 4:
            no_inline += 1
    templates = template_records(sequence_counter, first, last, reference["execution_templates"][side])
    reference_map = {tuple(item["sequence"]): item["rows"] for item in reference["execution_templates"][side]}
    require(dict(sequence_counter) == reference_map, (side, "template sequence/count"))
    require(len(sequence_counter) == (1 if side == "client" else 25), (side, "template count"))
    require(set(selector_values) == {0}, (side, "selector bytes"))
    require(marker_counts["colour_tag"] == Counter({1: N}), (side, "colour marker"))
    require(marker_counts["stat_a_tag"] == Counter({2: N}), (side, "stat A marker"))
    require(marker_counts["stat_b_tag"] == Counter({3: N}), (side, "stat B marker"))
    require(marker_counts["wbcl_present"] == Counter({1: N}), (side, "wbcl marker"))
    row_trace = b"".join(pack("<III", row["start"], row["end"], uid) for row, uid in zip(rows, uids))
    identity_bytes = b"".join(payload[at : at + 12] for at in selected)
    return {
        "payload_sha256": digest(payload),
        "payload_size": len(payload),
        "candidate_histogram": histogram([len(group) for group in groups]),
        "candidate_total": sum(len(group) for group in groups),
        "candidate_alignment_counts": alignment_candidate_counts,
        "native_path": {
            "header": HEADER, "identity_width": 12, "footer": len(FOOTER),
            "positions_sha256": digest(b"".join(pack("<I", at) for at in selected)),
            "identity_bytes_sha256": digest(identity_bytes),
            "uid_sha256": digest(b"".join(pack("<I", uid) for uid in uids)),
            "row_trace_sha256": digest(row_trace),
            "first": [0, selected[0], uids[0]],
            "last": [N - 1, selected[-1], uids[-1]],
        },
        "row_width_histogram": histogram([row["width"] for row in rows]),
        "uid_sha256": digest(b"".join(pack("<I", uid) for uid in uids)),
        "uids": uids,
        "positions": selected,
        "rows": rows,
        "selector_histogram": histogram(selector_values),
        "selector_sha256": digest(bytes(selector_values)),
        "templates": templates,
        "template_count": len(sequence_counter),
        "event_values": event_values,
        "marker_histograms": {key: histogram(value) for key, value in marker_counts.items()},
        "no_inline_name_rows": no_inline,
        "following_zero_marker_rows": sum(payload[at + 12] == 0 for at in selected),
        "sensitivity": sensitivity,
        "footer_hex": payload[-len(FOOTER) :].hex(),
        "header_hex": payload[:HEADER].hex(),
    }


def crosswalk(archives: dict[str, Any], data: dict[str, dict[str, Any]], fixtures_result: dict[str, Any], reference_sha: str) -> dict[str, Any]:
    client = data["client"]
    server = data["server"]
    same_uids = client["uids"] == server["uids"]
    same_footer = client["footer_hex"] == server["footer_hex"] == FOOTER.hex()
    same_identity = client["native_path"]["identity_bytes_sha256"] == server["native_path"]["identity_bytes_sha256"]
    template_ok = all(item["matches_reference"] for item in server["templates"]) and server["template_count"] == 25
    claims = [
        {
            "id": "C1",
            "claim": "table_25 client/server members are independently selected by archive TOC and declared payload size",
            "method": "Parse both FMF TOCs, bound table_25 by the next member, decode every zstd frame, and select the unique frame whose output length equals the TOC declaration.",
            "evidence": {side: archives[side] for side in SIDES},
            "grade": "L2",
            "status": "pass",
        },
        {
            "id": "C2",
            "claim": "The native 12-byte identity plus 9-byte footer closes exactly once on both archives.",
            "method": "Scan all four byte alignments for ordinal|UID|UID, then count non-overlapping full tilings by ordinal with UID nonzero and strictly increasing; recover the sole path.",
            "evidence": {side: {"paths": data[side]["sensitivity"]["native_identity"]["paths"], "positions_sha256": data[side]["native_path"]["positions_sha256"], "row_width_histogram": data[side]["row_width_histogram"], "alignment_candidate_counts": data[side]["candidate_alignment_counts"]} for side in SIDES},
            "grade": "L2",
            "status": "pass" if all(data[side]["sensitivity"]["native_identity"]["paths"] == 1 for side in SIDES) else "fail",
        },
        {
            "id": "C3",
            "claim": "The 7,047 identity UIDs align client-to-server byte-for-byte as a data-side result independent of the reader cursor.",
            "method": "Compare recovered ordinal and UID lanes, the concatenated 12-byte identity digest, and UID digest after two independent DP recoveries.",
            "evidence": {"uid_equal": same_uids, "identity_bytes_sha256_equal": same_identity, "uid_sha256_client": client["uid_sha256"], "uid_sha256_server": server["uid_sha256"]},
            "grade": "L2",
            "status": "pass" if same_uids and same_identity else "fail",
        },
        {
            "id": "C4",
            "claim": "The footer is identical in both archives, byte-for-byte.",
            "method": "Read the nine bytes after the recovered final identity and compare both payloads to the frozen byte string.",
            "evidence": {"client": client["footer_hex"], "server": server["footer_hex"], "expected": FOOTER.hex()},
            "grade": "L2",
            "status": "pass" if same_footer else "fail",
        },
        {
            "id": "C5",
            "claim": "All 7,047 selector bytes are zero; server row byte sequences match the 25 t59 execution templates and counts.",
            "method": "Parse only row bytes between recovered boundaries, record the first selector and each byte-grammar event in order, then compare the resulting sequence/count map to t59 field_slots.json; no CFG is rebuilt.",
            "evidence": {"client_selector_histogram": client["selector_histogram"], "server_selector_histogram": server["selector_histogram"], "server_template_count": server["template_count"], "reference_sha256": reference_sha, "template_matches": template_ok},
            "grade": "L2",
            "status": "pass" if template_ok and client["selector_histogram"] == {"0": N} and server["selector_histogram"] == {"0": N} else "fail",
        },
        {
            "id": "C6",
            "claim": "The t01f six-continent, parent-352, England, and China PR fixtures re-close on both row sets.",
            "method": "Use recovered row ordinals and byte-grammar event coordinates to recheck the named t01f values, child parent ordinal, parent UID, and identity UID anchors.",
            "evidence": fixtures_result,
            "grade": "L2",
            "status": "pass",
        },
    ]
    return {
        "task": "t67",
        "table": 25,
        "scope": "COMP table_25 data-side crosswalk only",
        "grade_target": "L2",
        "L3": 0,
        "L4": 0,
        "source": {"data_dir": DATA.as_posix(), "t59_reference": T59.as_posix(), "t59_reference_sha256": reference_sha, "t59_fixture_reference": (ROOT / "scratch/t59/out/field_map.json").as_posix(), "t59_fixture_reference_sha256": digest((ROOT / "scratch/t59/out/field_map.json").read_bytes()), "t01f": T01F.as_posix()},
        "claims": claims,
        "archives": archives,
        "native_identity": {side: data[side]["native_path"] for side in SIDES},
        "selectors": {side: {"histogram": data[side]["selector_histogram"], "sha256": data[side]["selector_sha256"], "marker_histograms": data[side]["marker_histograms"]} for side in SIDES},
        "templates": {side: data[side]["templates"] for side in SIDES},
        "identity_crosswalk": {"uid_equal": same_uids, "uid_sha256": {"client": client["uid_sha256"], "server": server["uid_sha256"]}, "identity_bytes_equal": same_identity, "footer_equal": same_footer, "uid_count": N},
        "fixtures": fixtures_result,
        "negative": [
            "13B marker/lookahead alternatives are retained as sensitivity controls; they do not replace the native 12B identity conclusion.",
            "Header 11..15 alternatives are data-compatible under the t59 lookahead model and therefore do not prove a header split.",
            "Relaxing UID nonzero/order increases the candidate path count; these are controls, not accepted framings.",
            "No field semantic is promoted beyond the t01f/t59 byte anchors; this deliverable does not claim L3 or L4.",
        ],
    }


def report(cw: dict[str, Any], sensitivity: dict[str, Any]) -> str:
    c = cw["identity_crosswalk"]
    lines = [
        "# t67 - COMP table_25 data-side crosswalk",
        "",
        "Status: complete. Evidence target: L2 data-side cross-validation. L3=0, L4=0.",
        "",
        "## Native envelope",
        "",
        "- client: 7,047 rows, 127 B each, 13 B header + 894,969 B rows + 9 B footer.",
        "- server: 7,047 rows, variable 198..1,894 B, 13 B header + 1,533,950 B rows + 9 B footer.",
        "- Both independent four-alignment scans and ordinal-layer non-overlap DP recover exactly one path with 12 B identity and UID nonzero/strictly increasing.",
        f"- UID lanes equal: {c['uid_equal']}; 12 B identity bytes equal: {c['identity_bytes_equal']}; footer equal: {c['footer_equal']}.",
        f"- Footer bytes: client `{cw['archives']['client']['payload_sha256']}`; server `{cw['archives']['server']['payload_sha256']}`; both end in `{FOOTER.hex()}`.",
        "",
        "## Selectors and templates",
        "",
        "- Client selector histogram: `{" + "0:7047" + "}`.",
        "- Server selector histogram: `{" + "0:7047" + "}`.",
        "- The byte-level row grammar yields one client template and 25 server templates. Sequence/count comparison to t59 `field_slots.json` is exact; no CFG is rebuilt here.",
        "",
        "## Sensitivity",
        "",
        "| control | client paths | server paths |",
        "|---|---:|---:|",
    ]
    names = [
        "identity_12_footer_7", "identity_12_footer_8", "identity_12_footer_9", "identity_12_footer_10", "identity_12_footer_12",
        "marker_0_footer_7", "marker_0_footer_8", "marker_0_footer_9", "marker_0_footer_10", "marker_0_footer_12",
        "triple_footer_7", "triple_footer_8", "triple_footer_9", "triple_footer_10", "triple_footer_12",
        "header_11", "header_12", "header_13", "header_14", "header_15",
        "selector_lookahead", "no_marker", "allow_zero", "no_uid_order", "both_relaxed", "wire_triple", "triple_no_lookahead", "native_identity",
    ]
    for name in names:
        lines.append(f"| `{name}` | {sensitivity['client'][name]['paths']} | {sensitivity['server'][name]['paths']} |")
    lines += [
        "",
        "The `both_relaxed` client result is capped at 1,000,000; server remains 4. `allow_zero` and `no_uid_order` are single-relaxation controls in the t59 model. The client fixed-width controls are recorded in `sensitivity.json`: tail-aligned 12B, 13B, and 8B assumptions plus the explicit 13B lookahead/footer-8 control.",
        "",
        "## t01f fixtures",
        "",
        "- Live continent ordinals are exactly `{0,1,2,3,4,5}` on both sides.",
        "- Rows 707 and 708 point to parent ordinal 352; ordinal 352 has UID 150990.",
        "- England `cnti` ordinal 139 and China PR `cnti` ordinal 55 reclose in comp rows on both sides; target nation UIDs 765 and 110 are the frozen t59 L2 fixture values (table_10 is not read here).",
        "- The 10 named continent/nation anchors and 2 parent anchors are rechecked with client coordinates and server values.",
        "",
        "## Boundaries",
        "",
        "- This is a data-side crosswalk for table_25 only. It does not change `reports/`, `scratch/t59/`, or any schema semantic assignment.",
        "- Candidate alternatives and negative controls remain in `sensitivity.json`; they are not promoted to native framing.",
        "- No game, editor, IDA, network, or `Z:` access was used.",
        "",
        "## Reproduction",
        "",
        "```text",
        "FM24_DB_DIR=<WORKSPACE>/scratch/data py -V:3.12 -I -B scripts/t67_comp_data_crosswalk.py --build",
        "FM24_DB_DIR=<WORKSPACE>/scratch/data py -V:3.12 -I -B scratch/t67/out/verify.py --check",
        "py -V:3.12 -I -B scripts/t01_anchors.py",
        "```",
        "",
    ]
    return "\n".join(lines)


def build() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    zstd = zstd_module()
    reference = json.loads(T59.read_text(encoding="utf-8"))
    reference_sha = digest(T59.read_bytes())
    payloads: dict[str, bytes] = {}
    archives: dict[str, Any] = {}
    for side in SIDES:
        payloads[side], archives[side] = load_table25(zstd, side)
    all_data = {side: process_side(payloads[side], side, reference) for side in SIDES}
    fixed = {
        "client_fixed_127B_tail_aligned_12B_footer_9": fixed_client_assumption(payloads["client"], 12, 9),
        "client_fixed_127B_tail_aligned_13B_footer_9": fixed_client_assumption(payloads["client"], 13, 9),
        "client_fixed_127B_tail_aligned_8B_footer_9": fixed_client_assumption(payloads["client"], 8, 9),
        "client_fixed_127B_13B_lookahead_footer_8": fixed_client_assumption(payloads["client"], 13, 8, lookahead=True),
    }
    fixtures_result = fixtures(all_data, payloads)
    sensitivity = {
        "task": "t67",
        "table": 25,
        "dp_definition": "four byte alignments; ordinal-layer candidates; non-overlap means previous_at + identity_width <= next_at; final candidate ends at payload-footer",
        "standard": "ordinal 0..7046, UID nonzero and strictly increasing, identity triple UID lane repeated",
        "sides": {side: all_data[side]["sensitivity"] for side in SIDES},
        "client_fixed_width_controls": fixed,
        "candidate_scan": {side: {"total": all_data[side]["candidate_total"], "histogram": all_data[side]["candidate_histogram"], "alignment_counts": all_data[side]["candidate_alignment_counts"]} for side in SIDES},
        "native": {side: all_data[side]["native_path"] for side in SIDES},
        "reference_t59_sensitivity_names": ["marker_0_footer_*", "header_11..15", "triple_footer_*", "selector_lookahead", "no_marker", "allow_zero", "no_uid_order", "both_relaxed", "wire_triple", "triple_no_lookahead"],
        "negative": [
            "13B lookahead controls can borrow the next selector or first footer byte; they are retained only as sensitivity comparisons.",
            "Header 11..15 are not data-discriminated by this candidate model.",
            "8B and tail-aligned 13B client identity assumptions are tested separately from the explicit 13B lookahead model.",
        ],
    }
    cw = crosswalk(archives, all_data, fixtures_result, reference_sha)
    cw["sensitivity_summary"] = {
        "client_fixed_width_controls": fixed,
        "standard_paths": {side: all_data[side]["sensitivity"]["native_identity"]["paths"] for side in SIDES},
    }
    dump_json(OUT / "sensitivity.json", sensitivity)
    dump_json(OUT / "crosswalk.json", cw)
    (OUT / "REPORT.md").write_text(report(cw, {side: all_data[side]["sensitivity"] for side in SIDES}), encoding="ascii")
    (OUT / "DONE.md").write_text(
        "# t67 delivery\n\n"
        "- `crosswalk.json`: L2 claim/method/evidence/grade ledger.\n"
        "- `sensitivity.json`: four-alignment DP controls, t59 sensitivity ports, and client fixed-width controls.\n"
        "- `verify.py`: independent archive, DP, byte-grammar, identity, footer, template, and t01f verifier.\n"
        "- `REPORT.md`: human-readable result and negative boundaries.\n"
        "- `scripts/t67_comp_data_crosswalk.py`: builder with `--help` and `--selftest`.\n\n"
        "Commands:\n\n"
        "```text\n"
        "FM24_DB_DIR=<WORKSPACE>/scratch/data py -V:3.12 -I -B scripts/t67_comp_data_crosswalk.py --build\n"
        "FM24_DB_DIR=<WORKSPACE>/scratch/data py -V:3.12 -I -B scratch/t67/out/verify.py --selftest\n"
        "FM24_DB_DIR=<WORKSPACE>/scratch/data py -V:3.12 -I -B scratch/t67/out/verify.py --check\n"
        "py -V:3.12 -I -B scripts/t01_anchors.py\n"
        "```\n", encoding="ascii")
    print(f"t67 build PASS: {N} rows per side; output={OUT}")


def selftest() -> None:
    payload = bytearray(b"\0" * HEADER)
    payload += b"abc" + pack("<III", 0, 10, 10)
    payload += b"xy" + pack("<III", 1, 20, 20)
    payload += FOOTER
    groups = scan_triples(bytes(payload), 2)
    result, path = dp_paths(bytes(payload), groups, HEADER, len(FOOTER), 12, None, True, True, True)
    require(result["paths"] == 1 and path == [16, 30], (result, path))
    bad, _ = dp_paths(bytes(payload), groups, HEADER, 8, 12, None, True, True, False)
    require(bad["paths"] == 0, bad)
    fixed = fixed_client_assumption(bytes(payload), 12, len(FOOTER))
    require(fixed["paths"] == 0, fixed)
    print("t67 builder selftest PASS")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", action="store_true", help="decode table_25 and write scratch/t67/out")
    parser.add_argument("--selftest", action="store_true", help="run synthetic DP and fixed-width checks")
    args = parser.parse_args()
    try:
        if args.selftest:
            selftest()
        elif args.build or not args.selftest:
            build()
        return 0
    except BuildError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # pragma: no cover - fatal environment errors
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
