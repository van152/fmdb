"""Independent verifier for the t67 COMP table_25 data-side crosswalk.

This file deliberately does not import the t67 builder or any t59 module. It
reopens the two FMF archives, rescans identity candidates, reruns the DP, and
replays the byte-level row grammar before checking the delivered JSON.
"""
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

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
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


class VerifyError(RuntimeError):
    pass


def require(ok: Any, message: Any) -> None:
    if not ok:
        raise VerifyError(str(message))


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


def u32(data: bytes, at: int = 0) -> int:
    return unpack_from("<I", data, at)[0]


def histogram(values: list[int] | Counter[int]) -> dict[str, int]:
    counter = values if isinstance(values, Counter) else Counter(values)
    return {str(k): counter[k] for k in sorted(counter)}


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
        out = directory[pos : pos + width]
        pos += width
        return out

    def number() -> int:
        return unpack_from("<I", take(4))[0]

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


def load_table25(zstd, side: str) -> tuple[bytes, dict[str, Any]]:
    path = DATA / f"{side}_db.dat"
    require(path.is_file(), f"missing archive {path}")
    blob = path.read_bytes()
    base, entries = archive_entries(blob, zstd)
    member = f"{side}_db/table_25.dat"
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
        require(blob[pos : pos + 4] == ZSTD_MAGIC, f"zstd @{pos}")
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
    require(payload[:8] == TAD and u32(payload, 8) == N, "COMP header/count")
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
    groups: list[list[tuple[int, int]]] = [[] for _ in range(N)]
    for align in range(4):
        at = align
        while at + 12 <= len(payload):
            ordinal, uid, repeat = unpack_from("<III", payload, at)
            if ordinal < N and uid == repeat:
                groups[ordinal].append((at, uid))
            at += 4
    for group in groups:
        group.sort()
    return groups


def alignment_counts(payload: bytes) -> dict[str, int]:
    counts = [0, 0, 0, 0]
    for align in range(4):
        at = align
        while at + 12 <= len(payload):
            ordinal, uid, repeat = unpack_from("<III", payload, at)
            if ordinal < N and uid == repeat:
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
) -> tuple[dict[str, Any], list[int] | None]:
    limit = len(payload) - footer
    previous: list[tuple[int, int, int]] = []
    links: list[dict[int, int | None]] = []
    for ordinal, group in enumerate(groups):
        current: list[tuple[int, int, int]] = []
        back: dict[int, int | None] = {}
        previous_at = [item[0] for item in previous]
        prefix = [0]
        for _at, _uid, ways in previous:
            prefix.append(min(CAP, prefix[-1] + ways))
        for at, uid in group:
            if at < header or at + width > limit:
                continue
            if markers is not None and (at + 12 >= len(payload) or payload[at + 12] not in markers):
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
                back[at] = predecessor
        if not current:
            return {"paths": 0, "saturated": False, "first_dead_ordinal": ordinal, "first_rejected_candidate": list(group[0]) if group else None}, None
        previous = current
        links.append(back)
    final = [item for item in previous if item[0] + width == limit]
    total = min(CAP, sum(item[2] for item in final))
    result = {"paths": total, "saturated": total == CAP, "first_dead_ordinal": None, "first_rejected_candidate": None}
    if total != 1:
        return result, None
    chosen = final[0][0]
    path = [chosen]
    for link in reversed(links[1:]):
        chosen = link[chosen]
        require(chosen is not None, "DP predecessor")
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
    limit = len(payload) - footer
    positions: list[int] = []
    for ordinal in range(N):
        start = HEADER + ordinal * 127
        at = start + 127 - (12 if lookahead else width)
        if at + 12 > len(payload):
            return {"paths": 0, "reason": "triple outside payload", "first_dead_ordinal": ordinal}
        x, uid, repeat = unpack_from("<III", payload, at)
        marker_ok = not lookahead or (at + 12 < len(payload) and payload[at + 12] == 0)
        if x != ordinal or uid != repeat or uid == 0 or not marker_ok:
            return {"paths": 0, "reason": "row-end identity bytes do not satisfy assumption", "first_dead_ordinal": ordinal, "candidate": [at, x, uid, repeat]}
        if at + (13 if lookahead else width) > limit:
            return {"paths": 0, "reason": "footer closure", "first_dead_ordinal": ordinal}
        positions.append(at)
    closed = positions[-1] + (13 if lookahead else width) == limit
    return {
        "paths": 1 if closed else 0,
        "reason": "closed fixed-width row formula" if closed else "fixed-width footer does not close",
        "first_dead_ordinal": None if closed else N - 1,
        "row_width": 127,
        "identity_width": 13 if lookahead else width,
        "footer": footer,
        "positions_sha256": digest(b"".join(pack("<I", at) for at in positions)),
    }


class RowBytes:
    def __init__(self, payload: bytes, start: int, identity: int):
        self.payload = payload
        self.p = start
        self.identity = identity
        self.sequence: list[str] = []
        self.events: dict[str, dict[str, Any]] = {}

    def raw(self, width: int) -> bytes:
        require(width >= 0 and self.p + width <= self.identity, f"row span @{self.p}")
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
        except VerifyError as exc:
            raise VerifyError(f"{key} @{at}: {exc}") from exc
        self.sequence.append(key)
        self.events[key] = {"at": at, "width": self.p - at, "raw": self.payload[at:self.p].hex(), "value": None}

    def number(self, width: int, signed: bool = False) -> int:
        return int.from_bytes(self.raw(width), "little", signed=signed)


PRE = [
    ("selector", 1), ("m15c", 1), ("m15d", 1), ("colour_tag", 1),
    ("m120", 2), ("m124", 2), ("m128", 2), ("m12c", 2), ("m130", 2),
    ("m134", 1), ("m1a0", 1), ("m1a2", 1), ("m1a3", 1), ("m1a4", 1),
    ("m1a5", 1), ("stat_a_tag", 1), ("m198", 1), ("m199", 1),
    ("m19a", 1), ("m19b", 1), ("m19c", 1), ("m19d", 1), ("m19e", 1),
    ("stat_b_tag", 1), ("m189_197", 15), ("mf6", 1), ("m138", 4),
    ("m13c", 4), ("m58", 4), ("m60", 4), ("m70", 4), ("m68", 4), ("m150", 2),
]
EXT0 = [("m180", 2), ("mb8", 4), ("m188", 1), ("m184", 2), ("m186", 2), ("m182", 2), ("m160", 8), ("m168", 8), ("m170", 8), ("m178", 8)]
EXT1 = [("mf0", 4), ("m1a1", 1), ("m1a8", 1), ("mf4", 1), ("mf5", 1)]
POST = [("m148", 4), ("m152", 2), ("m154", 2), ("m156", 2), ("m158", 2), ("m15a", 2), ("m80", 4), ("m88", 4), ("m90", 4), ("m98", 4)]
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
            require(0 <= count <= identity - row.p, "vec30")
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
                require(row.number(4) == 0, "e0")
            row.dynamic("obj_e0", e0)

        def vec18() -> None:
            count = row.number(4, signed=True)
            require(0 <= count <= identity - row.p, "vec18")
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
                    require(0 <= inner <= identity - row.p, "c0 inner")
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
            require(count >= 0 and count <= identity - row.p, "vec100")
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
    require(row.p == identity + 12, (row.p, identity))
    return row.sequence, row.events


def row_layout(positions: list[int]) -> list[dict[str, int]]:
    limit = None
    rows = []
    for ordinal, identity in enumerate(positions):
        start = HEADER if ordinal == 0 else positions[ordinal - 1] + 12
        end = identity + 12
        require(start <= identity and end > start, (ordinal, start, identity, end))
        rows.append({"ordinal": ordinal, "start": start, "identity": identity, "end": end, "width": end - start})
    return rows


def template_records(counter: Counter[tuple[str, ...]], first: dict[tuple[str, ...], int], last: dict[tuple[str, ...], int], reference: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result = []
    for index, item in enumerate(reference):
        sequence = tuple(item["sequence"])
        result.append({
            "reference_index": index, "rows": counter.get(sequence, 0), "reference_rows": item["rows"],
            "first_ordinal": first.get(sequence), "last_ordinal": last.get(sequence), "sequence": list(sequence),
            "sequence_sha256": digest(json.dumps(list(sequence), separators=(",", ":")).encode("ascii")),
            "matches_reference": counter.get(sequence, 0) == item["rows"],
        })
    return result


def compute_side(payload: bytes, side: str, reference: dict[str, Any]) -> dict[str, Any]:
    groups = scan_triples(payload)
    alignment_candidate_counts = alignment_counts(payload)
    sensitivity = {}
    selected = None
    for name, args in options().items():
        result, path = dp_paths(payload, groups, *args)
        sensitivity[name] = result
        if name == "native_identity":
            require(result["paths"] == 1 and path is not None, (side, "native path"))
            selected = path
    require(selected is not None, "selected path")
    rows = row_layout(selected)
    uids = [u32(payload, at + 4) for at in selected]
    require([u32(payload, at) for at in selected] == list(range(N)), (side, "ordinal lane"))
    require(all(u32(payload, at + 8) == uid for at, uid in zip(selected, uids)), (side, "repeat lane"))
    require(all(uid > 0 for uid in uids) and all(a < b for a, b in zip(uids, uids[1:])), (side, "UID order"))
    require(payload[-9:] == FOOTER, (side, "footer"))
    counter: Counter[tuple[str, ...]] = Counter()
    first: dict[tuple[str, ...], int] = {}
    last: dict[tuple[str, ...], int] = {}
    events = {key: [None] * N for key in ("m58", "m60", "m68")}
    selectors = []
    markers = {key: Counter() for key in ("selector", "colour_tag", "stat_a_tag", "stat_b_tag", "wbcl_present")}
    for row in rows:
        sequence, row_events = parse_row(payload, row["start"], row["identity"], side == "server")
        key = tuple(sequence)
        counter[key] += 1
        first.setdefault(key, row["ordinal"])
        last[key] = row["ordinal"]
        for name in events:
            events[name][row["ordinal"]] = row_events[name]
        for name in markers:
            markers[name][row_events[name]["value"]] += 1
        selectors.append(row_events["selector"]["value"])
    ref_templates = reference["execution_templates"][side]
    require(dict(counter) == {tuple(item["sequence"]): item["rows"] for item in ref_templates}, (side, "templates"))
    templates = template_records(counter, first, last, ref_templates)
    return {
        "sensitivity": sensitivity,
        "positions": selected,
        "rows": rows,
        "uids": uids,
        "candidate_histogram": histogram([len(group) for group in groups]),
        "candidate_total": sum(len(group) for group in groups),
        "candidate_alignment_counts": alignment_candidate_counts,
        "selector_histogram": histogram(selectors),
        "selector_sha256": digest(bytes(selectors)),
        "templates": templates,
        "template_count": len(counter),
        "events": events,
        "marker_histograms": {key: histogram(value) for key, value in markers.items()},
        "native": {
            "header": HEADER, "identity_width": 12, "footer": 9,
            "positions_sha256": digest(b"".join(pack("<I", at) for at in selected)),
            "identity_bytes_sha256": digest(b"".join(payload[at:at + 12] for at in selected)),
            "uid_sha256": digest(b"".join(pack("<I", uid) for uid in uids)),
            "row_trace_sha256": digest(b"".join(pack("<III", row["start"], row["end"], uid) for row, uid in zip(rows, uids))),
            "first": [0, selected[0], uids[0]], "last": [N - 1, selected[-1], uids[-1]],
        },
        "uid_sha256": digest(b"".join(pack("<I", uid) for uid in uids)),
        "row_width_histogram": histogram([row["width"] for row in rows]),
        "footer_hex": payload[-9:].hex(),
    }


def fixture_result(data: dict[str, dict[str, Any]]) -> dict[str, Any]:
    prior = read_json(T01F)
    named = []
    for item in prior["verification"]["continent_and_nation_named_anchors"]:
        row = item["row_index"]
        result = {"row": row, "name": item["prior_english_name"], "uid": item["dbid"], "sides": {}}
        for side in SIDES:
            require(data[side]["uids"][row] == item["dbid"], (side, row, "named uid"))
            slots = {}
            for slot, field in (("m58", "ccti"), ("m60", "cnti")):
                event = data[side]["events"][slot][row]
                expected = bytes.fromhex(item[field]["bytes"].replace(" ", ""))
                require(event["value"] == int.from_bytes(expected, "little"), (side, row, field))
                if side == "client":
                    require(event["at"] == int(item[field]["payload_offset"], 16), (side, row, field, "at"))
                slots[field] = {"at": event["at"], "raw": event["raw"], "value": event["value"], "expected_raw": expected.hex()}
            result["sides"][side] = {"uid": data[side]["uids"][row], "slots": slots}
        named.append(result)
    parents = []
    for item in prior["verification"]["cpcm_named_anchors"]:
        row = item["row_index"]
        parent = item["expected_parent_ordinal"]
        result = {"child_row": row, "parent_ordinal": parent, "parent_uid": item["parent_dbid"], "sides": {}}
        for side in SIDES:
            event = data[side]["events"]["m68"][row]
            require(data[side]["uids"][row] == item["child_dbid"], (side, row, "child"))
            require(data[side]["uids"][parent] == item["parent_dbid"], (side, parent, "parent"))
            require(event["value"] == parent, (side, row, "parent ordinal"))
            result["sides"][side] = {"child_uid": data[side]["uids"][row], "parent_uid": data[side]["uids"][parent], "at": event["at"], "raw": event["raw"], "value": event["value"]}
        parents.append(result)
    continents = {}
    for side in SIDES:
        values = [data[side]["events"]["m58"][i]["value"] for i in range(N)]
        continents[side] = sorted({value for value in values if value != 0xFFFFFFFF})
        require(continents[side] == list(range(6)), (side, "continents"))
    field_map_path = ROOT / "scratch/t59/out/field_map.json"
    field_map_bytes = field_map_path.read_bytes()
    field_map = json.loads(field_map_bytes.decode("utf-8"))
    target_england = field_map["fixtures"]["England"]
    target_china = field_map["fixtures"]["China_PR"]
    england_rows = [7, 664]
    china_rows = [245, 250]
    england_values = {side: [data[side]["events"]["m60"][row]["value"] for row in england_rows] for side in SIDES}
    china_values = {side: [data[side]["events"]["m60"][row]["value"] for row in china_rows] for side in SIDES}
    require(all(values == [target_england[0]] * len(england_rows) for values in england_values.values()), england_values)
    require(all(values == [target_china[0]] * len(china_rows) for values in china_values.values()), china_values)
    return {"named_anchors": named, "parent_anchors": parents, "live_continent_ordinals": continents, "England": {"nation_ordinal": target_england[0], "nation_uid": {"client": target_england[1], "server": target_england[1]}, "comp_rows": england_rows, "comp_m60_values": england_values}, "China_PR": {"nation_ordinal": target_china[0], "nation_uid": {"client": target_china[1], "server": target_china[1]}, "comp_rows": china_rows, "comp_m60_values": china_values}, "negative_parent_ordinals": [], "target_fixture_reference": {"path": field_map_path.as_posix(), "sha256": digest(field_map_bytes)}}


def check() -> None:
    crosswalk = read_json(OUT / "crosswalk.json")
    sensitivity = read_json(OUT / "sensitivity.json")
    reference = read_json(T59)
    reference_sha = digest(T59.read_bytes())
    require(crosswalk["table"] == 25 and crosswalk["grade_target"] == "L2", "crosswalk header")
    require(crosswalk["source"]["t59_reference_sha256"] == reference_sha, "t59 reference digest")
    field_map_path = ROOT / "scratch/t59/out/field_map.json"
    require(crosswalk["source"]["t59_fixture_reference_sha256"] == digest(field_map_path.read_bytes()), "t59 fixture digest")
    require(len(crosswalk["claims"]) == 6 and all(item["status"] == "pass" and item["grade"] == "L2" for item in crosswalk["claims"]), "claim ledger")
    zstd = zstd_module()
    payloads: dict[str, bytes] = {}
    archives: dict[str, Any] = {}
    data: dict[str, dict[str, Any]] = {}
    for side in SIDES:
        payloads[side], archives[side] = load_table25(zstd, side)
        require(crosswalk["archives"][side] == archives[side], (side, "archive evidence"))
        data[side] = compute_side(payloads[side], side, reference)
        require(sensitivity["sides"][side] == data[side]["sensitivity"], (side, "sensitivity replay"))
        require(sensitivity["candidate_scan"][side] == {"total": data[side]["candidate_total"], "histogram": data[side]["candidate_histogram"], "alignment_counts": data[side]["candidate_alignment_counts"]}, (side, "candidate census"))
        require(crosswalk["native_identity"][side] == data[side]["native"], (side, "native evidence"))
        require(crosswalk["selectors"][side]["histogram"] == data[side]["selector_histogram"], (side, "selector histogram"))
        require(crosswalk["selectors"][side]["sha256"] == data[side]["selector_sha256"], (side, "selector digest"))
        require(crosswalk["templates"][side] == data[side]["templates"], (side, "template evidence"))
    require(data["client"]["uids"] == data["server"]["uids"], "client/server UID equality")
    require(data["client"]["native"]["identity_bytes_sha256"] == data["server"]["native"]["identity_bytes_sha256"], "identity equality")
    require(data["client"]["footer_hex"] == data["server"]["footer_hex"] == FOOTER.hex(), "footer equality")
    require(crosswalk["identity_crosswalk"] == {"uid_equal": True, "uid_sha256": {"client": data["client"]["uid_sha256"], "server": data["server"]["uid_sha256"]}, "identity_bytes_equal": True, "footer_equal": True, "uid_count": N}, "identity ledger")
    expected_fixtures = fixture_result(data)
    require(crosswalk["fixtures"] == expected_fixtures, "t01f fixture ledger")
    require(sensitivity["standard"] == "ordinal 0..7046, UID nonzero and strictly increasing, identity triple UID lane repeated", "standard wording")
    fixed = sensitivity["client_fixed_width_controls"]
    require(fixed["client_fixed_127B_tail_aligned_12B_footer_9"]["paths"] == 1, "client fixed 12B")
    require(fixed["client_fixed_127B_tail_aligned_13B_footer_9"]["paths"] == 0, "client fixed 13B")
    require(fixed["client_fixed_127B_tail_aligned_8B_footer_9"]["paths"] == 0, "client fixed 8B")
    require(fixed["client_fixed_127B_13B_lookahead_footer_8"]["paths"] == 1, "client lookahead")
    require(sensitivity["sides"]["client"]["native_identity"]["paths"] == 1 and sensitivity["sides"]["server"]["native_identity"]["paths"] == 1, "native uniqueness")
    print("t67 independent PASS: 7047 client + 7047 server; native identity/footer, selectors, 25 templates, and t01f fixtures closed")


def selftest() -> None:
    payload = b"\0" * HEADER + b"abc" + pack("<III", 0, 10, 10) + b"xy" + pack("<III", 1, 20, 20) + FOOTER
    groups = [[] for _ in range(2)]
    for align in range(4):
        at = align
        while at + 12 <= len(payload):
            ordinal, uid, repeat = unpack_from("<III", payload, at)
            if ordinal < 2 and uid == repeat:
                groups[ordinal].append((at, uid))
            at += 4
    for group in groups:
        group.sort()
    result, path = dp_paths(payload, groups, HEADER, len(FOOTER), 12, None, True, True)
    require(result["paths"] == 1 and path == [16, 30], (result, path))
    wrong, _ = dp_paths(payload, groups, HEADER, 8, 12, None, True, True)
    require(wrong["paths"] == 0, wrong)
    print("t67 verifier selftest PASS")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="rerun the independent full verification")
    parser.add_argument("--selftest", action="store_true", help="run synthetic DP checks")
    args = parser.parse_args()
    try:
        if args.selftest:
            selftest()
        else:
            check()
        return 0
    except VerifyError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # pragma: no cover - fatal environment errors
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
