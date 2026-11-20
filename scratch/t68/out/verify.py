#!/usr/bin/env python3
"""Independent full verifier for the t68 Club table_3 crosswalk."""
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

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
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


class VerifyError(RuntimeError):
    pass


def require(condition: Any, message: Any) -> None:
    if not condition:
        raise VerifyError(str(message))


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


def read_json(path: Path) -> Any:
    require(path.is_file(), f"missing {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def u32(data: bytes, at: int = 0) -> int:
    return unpack_from("<I", data, at)[0]


def histogram(values: list[int] | Counter[int]) -> dict[str, int]:
    counts = values if isinstance(values, Counter) else Counter(values)
    return {str(key): counts[key] for key in sorted(counts)}


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
    toc, base = toc_rel + 17, base_rel + 17
    require(blob[toc : toc + 9] == blob[8:17], "FMF TOC shell")
    decoder = zstd.ZstdDecompressor().decompressobj()
    directory = decoder.decompress(blob[toc + 9 :])
    used = len(blob) - (toc + 9) - len(decoder.unused_data)
    require(decoder.eof and toc + 9 + used == len(blob), "TOC closure")
    cursor = 0
    entries: dict[str, tuple[int, int, int]] = {}

    def take(width: int) -> bytes:
        nonlocal cursor
        require(cursor + width <= len(directory), "short TOC")
        result = directory[cursor : cursor + width]
        cursor += width
        return result

    def number() -> int:
        return u32(take(4))

    def text() -> str:
        return take(number()).decode("utf-8")

    def walk(parent: PurePosixPath, depth: int) -> None:
        require(depth < 40, "TOC recursion")
        folder = parent / text()
        for _ in range(number()):
            name = (folder / (text() + text())).as_posix()
            require(name not in entries and ".." not in PurePosixPath(name).parts, "unsafe or duplicate TOC path")
            offset, span, size, _a, _b = unpack_from("<5Q", take(40))
            entries[name] = (base + offset, span, size)
        for _ in range(number()):
            walk(folder, depth + 1)

    walk(PurePosixPath(), 0)
    require(cursor == len(directory), "TOC trailing bytes")
    return base, entries


def load_table3(zstd, side: str) -> tuple[bytes, dict[str, Any]]:
    archive_path = DATA / f"{side}_db.dat"
    require(archive_path.is_file(), f"missing archive {archive_path}")
    archive = archive_path.read_bytes()
    base, entries = archive_entries(archive, zstd)
    member = f"{side}_db/table_3.dat"
    require(member in entries, f"missing {member}")
    start, packed_size, declared_size = entries[member]
    end = start + packed_size
    toc = unpack_from("<QQ", archive, 17)[0] + 17
    next_entry = min((offset for offset, _span, _size in entries.values() if offset > start), default=toc)
    require(base <= start < end <= next_entry <= len(archive), "member bounds")
    packed = archive[start:end]
    position = start
    frames: list[list[int]] = []
    candidates: list[bytes] = []
    while position < end:
        require(archive[position : position + 4] == ZSTD_MAGIC, f"zstd frame magic @{position}")
        decoder = zstd.ZstdDecompressor().decompressobj()
        payload = decoder.decompress(archive[position:end])
        frame_size = end - position - len(decoder.unused_data)
        require(decoder.eof and frame_size > 0, "invalid zstd frame")
        frames.append([position, position + frame_size, len(payload)])
        if len(payload) == declared_size:
            candidates.append(payload)
        position += frame_size
    require(position == end and len(candidates) == 1, "unique declared-size frame")
    payload = candidates[0]
    require(payload[:8] == TAD and u32(payload, 8) == N, f"{side} table_3 header/count")
    return payload, {
        "archive": archive_path.as_posix(),
        "archive_sha256": digest(archive),
        "member": member,
        "data_base": base,
        "range": [start, end],
        "bound": next_entry,
        "declared_size": declared_size,
        "frames": frames,
        "packed_sha256": digest(packed),
        "payload_sha256": digest(payload),
        "count": u32(payload, 8),
    }


def scan_candidates(payload: bytes, triple: bool) -> list[list[tuple[int, int]]]:
    groups: list[list[tuple[int, int]]] = [[] for _ in range(N)]
    try:
        import numpy as np  # type: ignore
    except ImportError:
        width_words = 3 if triple else 2
        for alignment in range(4):
            at = alignment
            while at + 4 * width_words <= len(payload):
                ordinal = u32(payload, at)
                uid = u32(payload, at + 4)
                if ordinal < N and (not triple or uid == u32(payload, at + 8)):
                    groups[ordinal].append((at, uid))
                at += 4
    else:
        for alignment in range(4):
            words = np.frombuffer(payload, dtype="<u4", offset=alignment, count=(len(payload) - alignment) // 4)
            if triple:
                hits = np.flatnonzero((words[:-2] < N) & (words[1:-1] == words[2:]))
            else:
                hits = np.flatnonzero(words[:-1] < N)
            for raw_index in hits:
                index = int(raw_index)
                ordinal, uid = int(words[index]), int(words[index + 1])
                groups[ordinal].append((alignment + index * 4, uid))
    for group in groups:
        group.sort()
    return groups


def candidate_alignment_counts(groups: list[list[tuple[int, int]]]) -> dict[str, int]:
    counts = [0, 0, 0, 0]
    for group in groups:
        for at, _uid in group:
            counts[at & 3] += 1
    return {str(index): value for index, value in enumerate(counts)}


class EpochFenwick:
    """Fenwick sums with generation stamps to reuse storage between layers."""

    def __init__(self, size: int):
        self.sums = [0] * (size + 1)
        self.last = [-1] * (size + 1)
        self.epochs = [0] * (size + 1)
        self.epoch = 0

    def begin(self) -> None:
        self.epoch += 1

    def add(self, index: int, amount: int, position: int) -> None:
        index += 1
        while index < len(self.sums):
            if self.epochs[index] != self.epoch:
                self.epochs[index] = self.epoch
                self.sums[index] = 0
                self.last[index] = -1
            self.sums[index] = min(CAP, self.sums[index] + amount)
            self.last[index] = max(self.last[index], position)
            index += index & -index

    def query(self, index: int) -> tuple[int, int]:
        total, witness = 0, -1
        index += 1
        while index > 0:
            if self.epochs[index] == self.epoch:
                total = min(CAP, total + self.sums[index])
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
    coords: list[int] | None = None,
    recover: bool = False,
    with_layers: bool = False,
) -> tuple[dict[str, Any], list[int] | None, dict[str, list[int]] | None]:
    limit = len(payload) - footer
    previous: list[tuple[int, int, int]] = []
    backlinks: list[dict[int, int | None]] = []
    layer_values = {key: [] for key in ("candidate_counts", "eligible_counts", "state_counts", "partial_path_mass")} if with_layers else None
    first_dead: int | None = None
    first_rejected: list[int] | None = None
    uid_coords = coords
    tree = None
    if increasing:
        if uid_coords is None:
            uid_coords = sorted({uid for group in groups for _at, uid in group})
        uid_positions = {uid: index for index, uid in enumerate(uid_coords)}
        tree = EpochFenwick(len(uid_coords))
    else:
        uid_positions = {}

    for ordinal, group in enumerate(groups):
        eligible = [
            (at, uid) for at, uid in group
            if at >= header and at + width <= limit
            and (markers is None or (at + 12 < len(payload) and payload[at + 12] in markers))
            and (not nonzero or uid != 0)
        ]
        current: list[tuple[int, int, int]] = []
        back: dict[int, int | None] = {}
        if ordinal == 0:
            for at, uid in eligible:
                current.append((at, uid, 1))
                if recover:
                    back[at] = None
        elif not increasing:
            prefix = [0]
            prefix_witness = [-1]
            for at, _uid, ways in previous:
                prefix.append(min(CAP, prefix[-1] + ways))
                prefix_witness.append(at if ways else prefix_witness[-1])
            previous_positions = [item[0] for item in previous]
            for at, uid in eligible:
                count = bisect_right(previous_positions, at - width)
                ways = prefix[count]
                if ways:
                    current.append((at, uid, ways))
                    if recover:
                        back[at] = prefix_witness[count]
        else:
            assert tree is not None and uid_coords is not None
            tree.begin()
            previous_index = 0
            for at, uid in eligible:
                while previous_index < len(previous) and previous[previous_index][0] + width <= at:
                    prev_at, prev_uid, prev_ways = previous[previous_index]
                    tree.add(uid_positions[prev_uid], prev_ways, prev_at)
                    previous_index += 1
                uid_index = bisect_left(uid_coords, uid) - 1
                ways, witness = tree.query(uid_index) if uid_index >= 0 else (0, -1)
                if ways:
                    current.append((at, uid, ways))
                    if recover:
                        back[at] = witness if witness >= 0 else None
        if layer_values is not None:
            layer_values["candidate_counts"].append(len(group))
            layer_values["eligible_counts"].append(len(eligible))
            layer_values["state_counts"].append(len(current))
            layer_values["partial_path_mass"].append(min(CAP, sum(state[2] for state in current)))
        if not current:
            first_dead = ordinal
            first_rejected = list(group[0]) if group else None
            return {
                "paths": 0,
                "saturated": False,
                "first_dead_ordinal": first_dead,
                "first_rejected_candidate": first_rejected,
                "processed_ordinals": ordinal + 1,
            }, None, layer_values
        previous = current
        if recover:
            backlinks.append(back)

    terminal = [item for item in previous if item[0] + width == limit]
    total = min(CAP, sum(item[2] for item in terminal))
    result = {
        "paths": total,
        "saturated": total == CAP,
        "first_dead_ordinal": first_dead,
        "first_rejected_candidate": first_rejected,
        "processed_ordinals": len(groups),
        "terminal_candidates": len(terminal),
    }
    if not recover or total != 1:
        return result, None, layer_values
    position = terminal[0][0]
    path = [position]
    for links in reversed(backlinks[1:]):
        position = links[position]
        require(position is not None, "missing predecessor")
        path.append(position)
    path.reverse()
    return result, path, layer_values


def summarize_layers(layers: dict[str, list[int]]) -> dict[str, Any]:
    blob = b"".join(pack("<I", value) for key in layers for value in layers[key])
    states, mass = layers["state_counts"], layers["partial_path_mass"]
    return {
        "count": len(states),
        "arrays": layers,
        "sha256": digest(blob),
        "single_state_layers": sum(value == 1 for value in states),
        "ambiguous_state_layers": sum(value > 1 for value in states),
        "single_partial_path_layers": sum(value == 1 for value in mass),
        "ambiguous_partial_path_layers": sum(value > 1 for value in mass),
        "max_state_count": max(states),
        "max_partial_path_mass": max(mass),
    }


def sensitivity(payload: bytes, triples: list[list[tuple[int, int]]], pairs: list[list[tuple[int, int]]]) -> tuple[dict[str, Any], list[int], dict[str, Any]]:
    controls: dict[str, tuple[list[list[tuple[int, int]]], int, int, int, set[int] | None, bool, bool]] = {}
    for footer in (7, 8, 9, 10, 12):
        controls[f"identity_12_footer_{footer}"] = (triples, HEADER, footer, 12, None, True, True)
        controls[f"identity_13_footer_{footer}_marker0"] = (triples, HEADER, footer, 13, {0}, True, True)
        controls[f"identity_13_footer_{footer}_no_marker"] = (triples, HEADER, footer, 13, None, True, True)
        controls[f"identity_8_footer_{footer}"] = (pairs, HEADER, footer, 8, None, True, True)
    for header in range(11, 16):
        controls[f"header_{header}"] = (triples, header, 8, 13, {0, 12}, True, True)
    controls.update({
        "selector_lookahead_13_footer_8": (triples, HEADER, 8, 13, {0, 12}, True, True),
        "triple_12_lookahead_footer_9": (triples, HEADER, 9, 12, {0, 12}, True, True),
        "no_marker_12_footer_9": (triples, HEADER, 9, 12, None, True, True),
        "allow_zero_12_footer_9": (triples, HEADER, 9, 12, {0, 12}, False, True),
        "no_uid_order_12_footer_9": (triples, HEADER, 9, 12, {0, 12}, True, False),
        "both_relaxed_12_footer_9": (triples, HEADER, 9, 12, {0, 12}, False, False),
    })
    triples_uids = sorted({uid for group in triples for _at, uid in group})
    pairs_uids = sorted({uid for group in pairs for _at, uid in group})
    results: dict[str, Any] = {}
    chosen: list[int] | None = None
    selected_layers: dict[str, Any] | None = None
    for name, (groups, header, footer, width, markers, nonzero, increasing) in controls.items():
        is_native = name == "no_marker_12_footer_9"
        coords = triples_uids if groups is triples else pairs_uids
        result, path, layers = dp_paths(
            payload, groups, header, footer, width, markers, nonzero, increasing,
            coords=coords, recover=is_native, with_layers=is_native,
        )
        results[name] = result
        if is_native:
            require(result["paths"] == 1 and path is not None and layers is not None, "native identity is not unique")
            chosen = path
            selected_layers = summarize_layers(layers)
    require(chosen is not None and selected_layers is not None, "missing native DP result")
    return results, chosen, selected_layers


SLOT_KEYS = [
    "selector", "derived_170", "derived_178", "ref_d8", "ref_e0", "ref_e8", "ref_f0", "ref_f8",
    "flags160", "name_len", "name_bytes", "short_len", "short_bytes", "raw16a", "raw166", "person148",
    "raw16c", "vec110", "obj150_tag", "obj150", "vec130", "vec138", "raw168", "stad140", "base_ba",
    "base_b8", "base18", "base30", "base60", "base78", "base90", "base48", "basea8", "identity",
]
SLOT_INDEX = {key: index for index, key in enumerate(SLOT_KEYS)}
PRE = [
    ("selector", 1), ("derived_170", 4), ("derived_178", 1), ("ref_d8", 4), ("ref_e0", 4),
    ("ref_e8", 4), ("ref_f0", 4), ("ref_f8", 4), ("flags160", 6), ("name_len", 4),
    ("name_bytes", None), ("short_len", 4), ("short_bytes", None),
]
EXT = [
    ("raw16a", 1), ("raw166", 2), ("person148", 4), ("raw16c", 1), ("vec110", 1),
    ("obj150_tag", 1), ("obj150", 45), ("vec130", 1), ("vec138", 1), ("raw168", 2), ("stad140", 4),
]
BASE = [("base18", 1), ("base30", 1), ("base60", 1), ("base78", 1), ("base90", 1), ("base48", 1), ("basea8", 2)]
ITEM_WIDTH = {
    "vec110": 4, "vec130": 24, "vec138": 12, "base18": 4, "base30": 4,
    "base60": 4, "base78": 4, "base90": 4, "base48": 16, "basea8": 28,
}


class RowParser:
    def __init__(self, payload: bytes, limit: int):
        self.payload = payload
        self.limit = limit
        self.position = HEADER
        self.order: list[str] = []
        self.spans: dict[str, list[tuple[int, int, int]]] = {key: [] for key in SLOT_KEYS}

    def take(self, row: int, key: str, width: int) -> int:
        at = self.position
        self.position += width
        require(width >= 0 and self.position <= self.limit, f"row {row} {key} span @{at}")
        self.order.append(key)
        self.spans[key].append((row, at, width))
        return at


def replay(payload: bytes, side: str, positions: list[int]) -> dict[str, Any]:
    parser = RowParser(payload, len(payload) - len(FOOTER))
    records: list[dict[str, int]] = []
    selectors: list[int] = []
    templates: Counter[tuple[int, ...]] = Counter()
    template_rows: dict[tuple[int, ...], list[int]] = {}
    row_templates: list[tuple[int, ...]] = []
    server = side == "server"
    for row in range(N):
        row_start, seq_start = parser.position, len(parser.order)
        selector_at = parser.take(row, "selector", 1)
        selector = payload[selector_at]
        require(selector in (0, 12), f"row {row}: invalid selector {selector}")
        selectors.append(selector)
        if selector == 12:
            parser.take(row, "derived_170", 4)
            parser.take(row, "derived_178", 1)
        for key, width in PRE[3:9]:
            parser.take(row, key, width)
        for label in ("name", "short"):
            length_at = parser.take(row, f"{label}_len", 4)
            length = u32(payload, length_at)
            require(length <= parser.limit - parser.position, f"row {row}: {label} length")
            if length:
                parser.take(row, f"{label}_bytes", length)
        if server:
            for key, width in EXT[:4]:
                parser.take(row, key, width)
            at = parser.take(row, "vec110", 1)
            count = payload[at]
            parser.position += count * ITEM_WIDTH["vec110"]
            require(parser.position <= parser.limit, f"row {row}: vec110 items")
            parser.spans["vec110"][-1] = (row, at, 1 + count * ITEM_WIDTH["vec110"])
            at = parser.take(row, "obj150_tag", 1)
            tag = payload[at]
            if tag == 0:
                parser.take(row, "obj150", 45)
            else:
                require(tag == 2, f"row {row}: unobserved obj150 tag {tag}")
            for key in ("vec130", "vec138"):
                at = parser.take(row, key, 1)
                count = payload[at]
                parser.position += count * ITEM_WIDTH[key]
                require(parser.position <= parser.limit, f"row {row}: {key} items")
                parser.spans[key][-1] = (row, at, 1 + count * ITEM_WIDTH[key])
            for key, width in EXT[9:]:
                parser.take(row, key, width)
            parser.take(row, "base_ba", 1)
            parser.take(row, "base_b8", 2)
            for key, width in BASE:
                at = parser.take(row, key, width)
                signed = key in ("base60", "base78")
                count = int.from_bytes(payload[at : at + width], "little", signed=signed)
                require(count >= 0, f"row {row}: negative {key} count")
                parser.position += count * ITEM_WIDTH[key]
                require(parser.position <= parser.limit, f"row {row}: {key} items")
                parser.spans[key][-1] = (row, at, width + count * ITEM_WIDTH[key])
        else:
            parser.take(row, "base_ba", 1)
            parser.take(row, "base_b8", 2)
        identity = parser.take(row, "identity", 12)
        require(identity == positions[row], f"row {row}: identity coordinate differs from DP")
        ordinal, uid, repeated = unpack_from("<III", payload, identity)
        require(ordinal == row and uid == repeated and uid != 0, f"row {row}: bad identity {(ordinal, uid, repeated)}")
        records.append({"ordinal": row, "start": row_start, "identity": identity, "end": parser.position, "width": parser.position - row_start, "uid": uid})
        template = tuple(SLOT_INDEX[key] for key in parser.order[seq_start:])
        templates[template] += 1
        template_rows.setdefault(template, []).append(row)
        row_templates.append(template)
    require(parser.position == parser.limit and payload[parser.position:] == FOOTER, f"{side}: footer closure")
    return {"rows": records, "book": parser.spans, "selectors": selectors, "templates": templates, "template_rows": template_rows, "row_templates": row_templates}


def template_records(observed: Counter[tuple[int, ...]], row_map: dict[tuple[int, ...], list[int]], reference: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for index, item in enumerate(reference):
        order = item["execution_order"]
        key = tuple(order)
        rows = observed.get(key, 0)
        ordinals = row_map.get(key, [])
        output.append({
            "reference_index": index,
            "rows": rows,
            "reference_rows": item["rows"],
            "first_ordinal": ordinals[0] if ordinals else None,
            "last_ordinal": ordinals[-1] if ordinals else None,
            "execution_order": list(order),
            "matches_reference": rows == item["rows"],
        })
    expected = {tuple(item["execution_order"]) for item in reference}
    require(set(observed) == expected, "unexpected row template")
    return output


def span_for(book: dict[str, list[tuple[int, int, int]]], name: str, row: int) -> tuple[int, int]:
    return next((at, width) for ordinal, at, width in book[name] if ordinal == row)


def fixture_witness(replays: dict[str, dict[str, Any]], identities: dict[str, list[tuple[int, int, int]]], maps: dict[str, Any]) -> dict[str, Any]:
    regression = maps["regression"]
    liverpool: dict[str, Any] = {"ordinal": 460, "uid": {}, "short_name": {}, "nation_ordinal": {}, "city_ordinal": {}}
    for side in SIDES:
        book, payload = replays[side]["book"], replays[side]["payload"]
        at, width = span_for(book, "short_bytes", 460)
        short_name = payload[at : at + width].decode("utf-8")
        nation_at, _ = span_for(book, "ref_d8", 460)
        city_at, _ = span_for(book, "ref_f8", 460)
        _ordinal, uid, _repeat = identities[side][460]
        liverpool["uid"][side] = uid
        liverpool["short_name"][side] = short_name
        liverpool["nation_ordinal"][side] = u32(payload, nation_at)
        liverpool["city_ordinal"][side] = u32(payload, city_at)
        require(uid == 676 and short_name == "Liverpool" and u32(payload, nation_at) == 139 and u32(payload, city_at) == 1061, f"{side}: Liverpool witness")
    bernabeu = regression["stadium"]["430"]
    founded = regression["founded_year_fixture_only"]
    liverpool_year = next(item for item in founded if item["row"] == 460)
    require(liverpool_year["year"] == 1892 and liverpool_year["external_year"] == 1892, "Liverpool year witness")
    return {
        "liverpool": liverpool,
        "bernabeu": {
            "source": "scratch/t57/out/field_map.json regression.stadium[430]",
            "stadium_ordinal": 430,
            "uid": 1056,
            "capacity": bernabeu["capacity_and_seats"][0],
            "seating_capacity": bernabeu["capacity_and_seats"][1],
            "city_ordinal": bernabeu["city_ordinal"],
            "rechecked_values": [bernabeu["uid"], bernabeu["capacity_and_seats"], bernabeu["city_ordinal"]],
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


def verify() -> None:
    crosswalk = read_json(OUT / "crosswalk.json")
    sensitivity_doc = read_json(OUT / "sensitivity.json")
    slots_bytes = T57.read_bytes()
    slots = json.loads(slots_bytes.decode("utf-8"))
    maps_bytes = T57_MAP.read_bytes()
    maps = json.loads(maps_bytes.decode("utf-8"))
    require(crosswalk["task"] == "t68" and crosswalk["table"] == 3 and crosswalk["entity"] == "club", "crosswalk identity")
    require(crosswalk["grade_target"] == "L2" and crosswalk["status"] == "complete_data_side_crosswalk", "crosswalk status/grade")
    require(crosswalk["scope"] == {
        "only_table_3": True, "rows_per_side": N, "reads_table_21": False,
        "reads_table_extra_3": False, "reads_club_link": False, "reads_editor_or_ida": False,
        "network": False, "z_drive": False,
    }, "scope ledger")
    require(crosswalk["source"]["t57_field_slots_sha256"] == digest(slots_bytes), "t57 field_slots digest")
    require(crosswalk["source"]["t57_field_map_sha256"] == digest(maps_bytes), "t57 field_map digest")
    require(len(crosswalk["claims"]) == 6 and all(item["status"] == "pass" and item["grade"] == "L2" for item in crosswalk["claims"]), "claim ledger")
    zstd = zstd_module()
    payloads: dict[str, bytes] = {}
    archive_records: dict[str, Any] = {}
    triple_groups: dict[str, list[list[tuple[int, int]]]] = {}
    pair_groups: dict[str, list[list[tuple[int, int]]]] = {}
    side_sensitivity: dict[str, Any] = {}
    chosen: dict[str, list[int]] = {}
    native_layers: dict[str, Any] = {}
    replays: dict[str, dict[str, Any]] = {}
    identity_values: dict[str, list[tuple[int, int, int]]] = {}
    native_records: dict[str, Any] = {}
    selector_records: dict[str, Any] = {}
    template_records_by_side: dict[str, Any] = {}
    candidate_records: dict[str, Any] = {}
    for side in SIDES:
        payloads[side], archive_records[side] = load_table3(zstd, side)
        require(crosswalk["archives"][side] == archive_records[side], f"{side}: archive record")
        triple_groups[side] = scan_candidates(payloads[side], True)
        pair_groups[side] = scan_candidates(payloads[side], False)
        side_sensitivity[side], chosen[side], native_layers[side] = sensitivity(payloads[side], triple_groups[side], pair_groups[side])
        require(sensitivity_doc["sides"][side] == side_sensitivity[side], f"{side}: sensitivity DP replay")
        triple_hist = histogram([len(group) for group in triple_groups[side]])
        pair_hist = histogram([len(group) for group in pair_groups[side]])
        candidate_records[side] = {
            "triple_total": sum(map(len, triple_groups[side])),
            "triple_histogram": triple_hist,
            "triple_alignment_counts": candidate_alignment_counts(triple_groups[side]),
            "pair_total": sum(map(len, pair_groups[side])),
            "pair_histogram": pair_hist,
            "pair_alignment_counts": candidate_alignment_counts(pair_groups[side]),
        }
        require(sensitivity_doc["candidate_scan"][side] == candidate_records[side], f"{side}: candidate scan")
        require(sensitivity_doc["native_layers"][side] == native_layers[side], f"{side}: per-ordinal DP layers")
        replays[side] = replay(payloads[side], side, chosen[side])
        replays[side]["payload"] = payloads[side]
        identity_values[side] = [unpack_from("<III", payloads[side], at) for at in chosen[side]]
        rows = replays[side]["rows"]
        uids = [item[1] for item in identity_values[side]]
        require(uids == [row["uid"] for row in rows], f"{side}: row/identity UID agreement")
        require(all(a < b for a, b in zip(uids, uids[1:])), f"{side}: UID order")
        require([item[0] for item in identity_values[side]] == list(range(N)), f"{side}: ordinal lane")
        require(all(item[1] == item[2] and item[1] != 0 for item in identity_values[side]), f"{side}: repeated UID lane")
        payload = payloads[side]
        native_records[side] = {
            "paths": side_sensitivity[side]["no_marker_12_footer_9"]["paths"],
            "header": HEADER,
            "identity_width": 12,
            "footer": 9,
            "positions": chosen[side],
            "positions_sha256": digest(b"".join(pack("<I", at) for at in chosen[side])),
            "identity_bytes_sha256": digest(b"".join(payload[at : at + 12] for at in chosen[side])),
            "uid_sha256": digest(b"".join(pack("<I", uid) for uid in uids)),
            "row_trace_sha256": digest(b"".join(pack("<III", row["start"], row["end"], row["uid"]) for row in rows)),
            "first": [0, chosen[side][0], uids[0]],
            "last": [N - 1, chosen[side][-1], uids[-1]],
            "row_width": [min(row["width"] for row in rows), max(row["width"] for row in rows)],
            "row_bytes": sum(row["width"] for row in rows),
            "footer_hex": payload[-9:].hex(),
        }
        require(crosswalk["native_identity"][side] == native_records[side], f"{side}: native identity/row trace")
        reference = slots["execution_templates"][side]
        observed_templates = template_records(replays[side]["templates"], replays[side]["template_rows"], reference)
        require(all(item["matches_reference"] for item in observed_templates), f"{side}: t57 execution order")
        template_records_by_side[side] = observed_templates
        selectors = replays[side]["selectors"]
        order_to_index = {tuple(item["execution_order"]): index for index, item in enumerate(reference)}
        template_index_sequence = [order_to_index[item] for item in replays[side]["row_templates"]]
        selector_records[side] = {
            "histogram": histogram(selectors),
            "sequence_hex": bytes(selectors).hex(),
            "sequence_sha256": digest(bytes(selectors)),
            "template_index_sequence": template_index_sequence,
            "template_index_sha256": digest(bytes(template_index_sequence)),
            "nonzero_rows": [index for index, value in enumerate(selectors) if value],
            "reference_execution_templates_sha256": digest(slots_bytes),
        }
        require(crosswalk["selectors"][side] == selector_records[side], f"{side}: selector sequence/template sequence")
        require(crosswalk["execution_templates"][side] == observed_templates, f"{side}: template counts/order")

    require([item[1] for item in identity_values["client"]] == [item[1] for item in identity_values["server"]], "UID lanes differ across archives")
    client_widths = [row["width"] for row in replays["client"]["rows"]]
    server_widths = [row["width"] for row in replays["server"]["rows"]]
    row_deltas = [server - client for client, server in zip(client_widths, server_widths, strict=True)]
    width_crosscheck = {
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
    require(width_crosscheck == {
        "client_row_bytes": 6_932_060,
        "server_row_bytes": 16_595_290,
        "client_width_min_max": [54, 156],
        "server_width_min_max": [81, 2618],
        "server_minus_client": {"rows": N, "all_positive": True, "min": 26, "max": 2547},
    }, "t57 paired row-width facts")
    require(crosswalk["row_width_crosscheck"] == width_crosscheck, "paired row-width ledger")
    identity_bytes_equal = all(
        payloads["client"][left : left + 12] == payloads["server"][right : right + 12]
        for left, right in zip(chosen["client"], chosen["server"], strict=True)
    )
    require(identity_bytes_equal, "identity bytes differ across archives")
    require(payloads["client"][-9:] == payloads["server"][-9:] == FOOTER, "footer bytes differ or incorrect")
    uid_digests = {side: native_records[side]["uid_sha256"] for side in SIDES}
    identity_digests = {side: native_records[side]["identity_bytes_sha256"] for side in SIDES}
    identity_crosswalk = {
        "uid_equal": True,
        "identity_bytes_equal": True,
        "footer_equal": True,
        "uid_count": N,
        "uid_sha256": uid_digests,
        "identity_sha256": identity_digests,
        "footer_hex": FOOTER.hex(),
    }
    require(crosswalk["identity_crosswalk"] == identity_crosswalk, "dual-archive identity ledger")
    require(sensitivity_doc["native_selected_positions"] == chosen, "selected identity positions")
    require(sensitivity_doc["dual_identity"] == identity_crosswalk, "sensitivity dual-identity ledger")
    require(sensitivity_doc["method"] == {
        "full_dp": True, "sampled": False, "processed_rows_per_side": N,
        "nonoverlap": True, "ordinal_layered": True, "path_count_cap": CAP,
        "cap_does_not_affect_uniqueness": True,
        "native_rule": "header 13; 12-byte ordinal|UID|UID identity; UID nonzero and strictly increasing; footer 9",
    }, "full-DP method declaration")
    expected_fixtures = fixture_witness(replays, identity_values, maps)
    require(crosswalk["fixtures"] == expected_fixtures, "Liverpool/Bernabeu/founded-year witnesses")
    require(all(crosswalk["t57_execution_template_match"][side] for side in SIDES), "t57 template match ledger")
    require(crosswalk["evidence_level"] == {"L1": 1, "L2": 1, "L3": 0, "L4": 0}, "evidence level")
    print("t68 independent verify PASS: 84,259 rows per side; full DP sensitivities, selectors, templates, identity, footer, and fixtures closed")


def selftest() -> None:
    payload = b"x" * HEADER + pack("<III", 0, 10, 10) + b"abc" + pack("<III", 1, 20, 20) + FOOTER
    groups = [[] for _ in range(2)]
    groups[0].append((HEADER, 10))
    groups[1].append((HEADER + 15, 20))
    result, path, layer_data = dp_paths(payload, groups, HEADER, 9, 12, None, True, True, coords=[10, 20], recover=True, with_layers=True)
    require(result["paths"] == 1 and path == [HEADER, HEADER + 15], (result, path))
    require(layer_data is not None and layer_data["state_counts"] == [1, 1], layer_data)
    wrong, _path, _layers = dp_paths(payload, groups, HEADER, 8, 12, None, True, True, coords=[10, 20])
    require(wrong["paths"] == 0, wrong)
    print("t68 independent verifier selftest PASS")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, epilog="Exit codes: 0 success, 1 check failure, 2 fatal/usage error.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="independently rerun the full crosswalk checks")
    group.add_argument("--selftest", action="store_true", help="run synthetic full-DP checks")
    args = parser.parse_args()
    try:
        if args.selftest:
            selftest()
        else:
            verify()
        return 0
    except VerifyError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # fatal environment, malformed archive, or programming error
        print(f"FATAL: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
