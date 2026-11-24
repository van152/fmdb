#!/usr/bin/env python3
"""t123: byte-exact basic_people_db decoder and name-pool report.

The basic_people file is a compact server wire stream.  This module keeps the
wire map separate from semantic observations so a false direct name join cannot
be mistaken for a proven L3 field.
"""
from __future__ import annotations
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg

import argparse
import datetime as _dt
import io
import json
import struct
import sys
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "scratch" / "t123" / "out"
BASIC_PATH = ROOT / "scratch" / "data" / "basic_people_db.dat"
ZSTD_SITE = Path(str(_cfg.VENDOR_DIR))
NAME_DIR = ROOT / "scratch" / "t106" / "out"

WIDTHS = {1: 83, 2: 83, 3: 83, 4: 34, 5: 22}
CLASS_NAMES = {
    1: "NON_PLAYER",
    2: "PLAYER",
    3: "ACTUAL_PLAYER_AND_NON_PLAYER",
    4: "OFFICIAL",
    5: "RETIRED_PERSON",
}
ANCHOR_UIDS = (28049320, 735216, 7458500)
SENTINEL_U32 = 0xFFFFFFFF

# These are read-chain results from people_db.dat.  The three IDs are looked up
# again in name_table_extra_{0,1,2}; they are not guessed display strings.
NAME_EVIDENCE: dict[int, dict[str, Any]] = {
    7458500: {"full_name": "Lionel Messi", "first": 174567, "second": 338403, "common": None, "birth_date": "1987-06-24"},
    18004457: {"full_name": "Kevin De Bruyne", "first": 24679, "second": 28741, "common": None, "birth_date": "1991-06-28"},
    85139014: {"full_name": "Kylian Mbapp\u00e9", "first": 223092, "second": 311441, "common": None, "birth_date": "1998-12-20"},
    29179241: {"full_name": "Erling Haaland", "first": 213966, "second": 414204, "common": None, "birth_date": "2000-07-21"},
    19302146: {"full_name": "Vin\u00edcius J\u00fanior", "first": 183409, "second": 362244, "common": 55642, "birth_date": "2000-07-12"},
    28049320: {"full_name": "Harry Kane", "first": 84138, "second": 228394, "common": None, "birth_date": "1993-07-28"},
    98028755: {"full_name": "Mohamed Salah", "first": 55580, "second": 132418, "common": None, "birth_date": "1992-06-15"},
    18026122: {"full_name": "Thibaut Courtois", "first": 24845, "second": 28641, "common": None, "birth_date": "1992-05-11"},
    55057659: {"full_name": "Ederson", "first": 176467, "second": 357061, "common": 63446, "birth_date": "1993-08-17"},
    67217524: {"full_name": "Rodri", "first": 229050, "second": 463296, "common": 78165, "birth_date": "1996-06-22"},
    719601: {"full_name": "Robert Lewandowski", "first": 35993, "second": 67164, "common": None, "birth_date": "1988-08-21"},
    37024025: {"full_name": "Virgil van Dijk", "first": 32288, "second": 56202, "common": None, "birth_date": "1991-07-08"},
    55041632: {"full_name": "Bernardo Silva", "first": 226852, "second": 457176, "common": None, "birth_date": "1994-08-10"},
    29232937: {"full_name": "Jude Bellingham", "first": 84393, "second": 233762, "common": None, "birth_date": "2003-06-29"},
    28106491: {"full_name": "Declan Rice", "first": 84261, "second": 228438, "common": None, "birth_date": "1999-01-14"},
    19058734: {"full_name": "Alisson", "first": 175802, "second": 42166, "common": 50143, "birth_date": "1992-10-02"},
    19024412: {"full_name": "Neymar", "first": 177069, "second": 362785, "common": 53855, "birth_date": "1992-02-05"},
    35017428: {"full_name": "Marc-Andr\u00e9 ter Stegen", "first": 28659, "second": 47605, "common": None, "birth_date": "1992-04-30"},
    28122642: {"full_name": "Bukayo Saka", "first": 85695, "second": 233113, "common": None, "birth_date": "2001-09-05"},
    92039023: {"full_name": "Joshua Kimmich", "first": 28419, "second": 46407, "common": None, "birth_date": "1995-02-08"},
    53095137: {"full_name": "Martin \u00d8degaard", "first": 213792, "second": 414168, "common": None, "birth_date": "1998-12-17"},
    14110660: {"full_name": "Lautaro Mart\u00ednez", "first": 174405, "second": 334228, "common": None, "birth_date": "1997-08-22"},
    55070299: {"full_name": "R\u00faben Dias", "first": 226838, "second": 457196, "common": None, "birth_date": "1997-05-14"},
    67086656: {"full_name": "Antoine Griezmann", "first": 223044, "second": 448987, "common": None, "birth_date": "1991-03-21"},
    653054: {"full_name": "Luka Modri\u0107", "first": 76257, "second": 173098, "common": None, "birth_date": "1985-09-09"},
    64016316: {"full_name": "Jan Oblak", "first": 81957, "second": 222452, "common": None, "birth_date": "1993-01-07"},
    43124203: {"full_name": "Bruno Fernandes", "first": 226826, "second": 457185, "common": None, "birth_date": "1994-09-08"},
    49056243: {"full_name": "Eduardo Camavinga", "first": 165575, "second": 324388, "common": None, "birth_date": "2002-11-10"},
    78085068: {"full_name": "Ronald Araujo", "first": 197418, "second": 388300, "common": None, "birth_date": "1999-03-07"},
    92020288: {"full_name": "Heung-Min Son", "first": 115513, "second": 272637, "common": None, "birth_date": "1992-07-08"},
    28108494: {"full_name": "Phil Foden", "first": 84165, "second": 236648, "common": None, "birth_date": "2000-05-28"},
    13158205: {"full_name": "Victor Osimhen", "first": 150056, "second": 306301, "common": None, "birth_date": "1998-12-29"},
    91138280: {"full_name": "Leroy San\u00e9", "first": 224729, "second": 309776, "common": None, "birth_date": "1996-01-11"},
    19306929: {"full_name": "Rodrygo", "first": 182412, "second": 359540, "common": 55895, "birth_date": "2001-01-09"},
    78074594: {"full_name": "Federico Valverde", "first": 197196, "second": 388723, "common": None, "birth_date": "1998-07-22"},
    85140178: {"full_name": "Ousmane Demb\u00e9l\u00e9", "first": 149573, "second": 304379, "common": None, "birth_date": "1997-05-15"},
    91003875: {"full_name": "\u0130lkay G\u00fcndo\u011fan", "first": 236725, "second": 495828, "common": None, "birth_date": "1990-10-24"},
    28060397: {"full_name": "John Stones", "first": 84129, "second": 228758, "common": None, "birth_date": "1994-05-28"},
    19273276: {"full_name": "\u00c9der Milit\u00e3o", "first": 182508, "second": 349622, "common": 54743, "birth_date": "1998-01-18"},
    92023410: {"full_name": "Antonio R\u00fcdiger", "first": 29251, "second": 48068, "common": None, "birth_date": "1993-03-03"},
    8435089: {"full_name": "Karim Benzema", "first": 223143, "second": 446412, "common": None, "birth_date": "1987-12-19"},
    37047745: {"full_name": "Frenkie de Jong", "first": 32477, "second": 56200, "common": None, "birth_date": "1997-05-12"},
    19220266: {"full_name": "Gabriel Jesus", "first": 185421, "second": 348156, "common": 52681, "birth_date": "1997-04-03"},
    19297055: {"full_name": "Bruno Guimar\u00e3es", "first": 180466, "second": 356645, "common": 63763, "birth_date": "1997-11-16"},
    49039004: {"full_name": "William Saliba", "first": 223135, "second": 311604, "common": None, "birth_date": "2001-03-24"},
    28067800: {"full_name": "Jack Grealish", "first": 84116, "second": 233647, "common": None, "birth_date": "1995-09-10"},
    28009441: {"full_name": "Kyle Walker", "first": 84176, "second": 227900, "common": None, "birth_date": "1990-05-28"},
    83111483: {"full_name": "Rafael Le\u00e3o", "first": 226839, "second": 459106, "common": None, "birth_date": "1999-06-10"},
    67022040: {"full_name": "Thiago", "first": 175672, "second": 353725, "common": 78894, "birth_date": "1991-04-11"},
    19163495: {"full_name": "Marquinhos", "first": 175691, "second": 363806, "common": 49982, "birth_date": "1994-05-14"},
    # Cristiano Ronaldo is an anchor but falls below the top 50 by PCAB.
    735216: {"full_name": "Cristiano Ronaldo", "first": 227709, "second": 457773, "common": 75689, "legal_name": "Cristiano Ronaldo dos Santos Aveiro", "birth_date": "1985-02-05"},
}

PERSON_24_FOURCC = [
    "PCDB", "PCcj", "PCij", "PScj", "PcJj", "Pcbi", "PcjN", "Pcob",
    "Pfke", "Pfrg", "Pife", "PkHs", "Ppfj", "Preg", "Prtg", "Pslr",
    "deit", "dept",
]


def _u8(row: bytes, off: int) -> int:
    return row[off]


def _u16(row: bytes, off: int) -> int:
    return struct.unpack_from("<H", row, off)[0]


def _u32(row: bytes, off: int) -> int:
    return struct.unpack_from("<I", row, off)[0]


def _pair(row: bytes, off: int) -> dict[str, int]:
    return {"ordinal": _u32(row, off), "uid": _u32(row, off + 4)}


def _hex_off(value: int | None) -> str | None:
    return None if value is None else f"0x{value:x}"


def _add_range(
    result: list[dict[str, Any]],
    start: int,
    width: int,
    mem_off: int | None,
    fourcc: str | None,
    semantic: str,
    *,
    aliases: Iterable[str] = (),
    class_name: str = "BASIC_PERSON",
    source: str = "140e4fd70.c + 140e50cd0.c",
    derived_mem_offs: Iterable[int] = (),
    note: str | None = None,
) -> None:
    for i in range(width):
        item: dict[str, Any] = {
            "wire_offset": start + i,
            "wire_byte": i,
            "wire_field_width": width,
            "class": class_name,
            "mem_off": _hex_off(mem_off),
            "mem_byte_offset": i,
            "fourcc": fourcc,
            "fourcc_aliases": list(aliases),
            "semantic": semantic,
            "source": source,
        }
        if derived_mem_offs:
            item["derived_mem_offs"] = [_hex_off(x) for x in derived_mem_offs]
        if note:
            item["note"] = note
        result.append(item)


def build_byte_map(kind: int) -> list[dict[str, Any]]:
    """Return one entry per serialized byte, with no omitted or merged bytes."""
    m: list[dict[str, Any]] = []
    _add_range(m, 0, 1, None, None, "record marker", class_name="WIRE", source="stream framing")
    _add_range(m, 1, 1, 0x65, "Ptyp", "person type", aliases=("Ptyp",))
    if kind in (1, 2, 3):
        _add_range(m, 2, 8, 0x30, "Pnti", "reference pair: nation/team-side", aliases=("Pnti",), note="reader W is runtime-selected 4/8; this file has the 8-byte form")
        _add_range(m, 10, 8, 0x20, "Pcti", "reference pair: current club/team", aliases=("Ptaj", "picc", "ptcn", "ptdn"), note="sub-object dereference in get_prop")
        _add_range(m, 18, 8, 0x28, "Pnai", "reference pair: auxiliary nation/affiliation", aliases=("Pnaj",), note="sub-object dereference in get_prop")
        _add_range(m, 26, 8, 0x38, None, "sub_140FB2BA0 helper payload", source="140e4fd70.c:80; helper definition not present in supplied funcs")
        _add_range(m, 34, 4, 0x48, "Pdva", "four-byte BASIC_PERSON field")
        _add_range(m, 38, 4, 0x4C, "Pcww", "four-byte BASIC_PERSON field")
        _add_range(m, 42, 2, 0x50, "PWRP", "world reputation", aliases=("Ascp", "Nwrr"))
        _add_range(m, 44, 2, 0x52, "PCRP", "current reputation", aliases=("Ncrr", "pnrc"), note="pnrc is an overlapping QWORD property; this wire read is 2 bytes")
        _add_range(m, 46, 2, 0x54, "PHRP", "home reputation", aliases=("Nhmr",))
        _add_range(m, 48, 2, 0x56, "PCAB", "current ability (CA)", aliases=("Ncra",))
        _add_range(m, 50, 2, 0x58, "PPAB", "potential ability (PA)", aliases=("Npta",))
        _add_range(m, 52, 2, 0x5A, "Pdob", "birth year/date packed field")
        _add_range(m, 54, 2, 0x5E, "PCJO", "job/secondary numeric field", aliases=("BPmj",))
        _add_range(m, 56, 2, 0x60, "PSJO", "job/secondary numeric field")
        _add_range(m, 58, 2, 0x62, "PNJO", "job/secondary numeric field")
        _add_range(m, 60, 1, 0x64, "Piap", "one-byte BASIC_PERSON field", aliases=("pcii",))
        _add_range(m, 61, 1, 0x66, "pcii", "adjacent pcii/Ptyp flag byte", aliases=("Ptyp",), note="0x66 is accessed by the pcii path; no separate canonical 4CC was recovered")
        _add_range(m, 62, 1, 0x68, "PLag", "language/flag byte")
        _add_range(m, 63, 8, 0x18, None, "PERSON base opaque qword", class_name="PERSON", aliases=PERSON_24_FOURCC, source="143f2b820.c:20; PERSON get_prop mappings")
        _add_range(m, 71, 4, 0x08, "PFxP", "PERSON identity ordinal", class_name="PERSON", source="143f2b820.c:31-48; PFxP mapping")
        _add_range(m, 75, 4, 0x08, "PFxP", "PERSON identity database ID", class_name="PERSON", source="143f2b820.c:31-48; PFxP mapping")
        _add_range(m, 79, 4, 0x08, "PFxP", "PERSON identity UID", class_name="PERSON", source="143f2b820.c:31-48; PFxP mapping")
    elif kind == 4:
        _add_range(m, 2, 8, 0x30, "Pnti", "reference pair: nation/team-side", aliases=("Pnti",), note="8-byte W form observed in the 34-byte OFFICIAL rows")
        _add_range(m, 10, 2, 0x52, "PCRP", "short-path reputation value", aliases=("Ncrr",), derived_mem_offs=(0x50, 0x54), note="140e4fd70.c:151-157 copies +82 to +80 and +84")
        _add_range(m, 12, 2, 0x5A, "Pdob", "birth year/date packed field")
        _add_range(m, 14, 8, 0x18, None, "PERSON base opaque qword", class_name="PERSON", aliases=PERSON_24_FOURCC, source="143f2b820.c:20; PERSON get_prop mappings")
        _add_range(m, 22, 4, 0x08, "PFxP", "PERSON identity ordinal", class_name="PERSON", source="143f2b820.c:31-48")
        _add_range(m, 26, 4, 0x08, "PFxP", "PERSON identity database ID", class_name="PERSON", source="143f2b820.c:31-48")
        _add_range(m, 30, 4, 0x08, "PFxP", "PERSON identity UID", class_name="PERSON", source="143f2b820.c:31-48")
    elif kind == 5:
        _add_range(m, 2, 8, 0x18, None, "PERSON base opaque qword", class_name="PERSON", aliases=PERSON_24_FOURCC, source="143f2b820.c:20; PERSON get_prop mappings")
        _add_range(m, 10, 4, 0x08, "PFxP", "PERSON identity ordinal", class_name="PERSON", source="143f2b820.c:31-48")
        _add_range(m, 14, 4, 0x08, "PFxP", "PERSON identity database ID", class_name="PERSON", source="143f2b820.c:31-48")
        _add_range(m, 18, 4, 0x08, "PFxP", "PERSON identity UID", class_name="PERSON", source="143f2b820.c:31-48")
    else:
        raise ValueError(kind)
    if len(m) != WIDTHS[kind] or [x["wire_offset"] for x in m] != list(range(WIDTHS[kind])):
        raise AssertionError(f"incomplete byte map type {kind}")
    return m


def load_zstandard() -> Any:
    if ZSTD_SITE.exists():
        sys.path.insert(0, str(ZSTD_SITE))
    try:
        import zstandard  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "zstandard is required; install/use the package under D:\\tmp2b\\fm24\\tools\\python"
        ) from exc
    return zstandard


def decompress_basic() -> tuple[bytes, int]:
    zstandard = load_zstandard()
    compressed = BASIC_PATH.read_bytes()
    if len(compressed) < 12 or compressed[:8] != bytes.fromhex("03017461642ef10d"):
        raise ValueError("unexpected Tad basic_people header")
    dctx = zstandard.ZstdDecompressor()
    with dctx.stream_reader(io.BytesIO(compressed[8:])) as reader:
        payload = reader.read()
    return payload, len(compressed)


def parse_basic(payload: bytes) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if len(payload) < 14:
        raise ValueError("basic_people payload too short")
    count = _u32(payload, 0)
    pos = 5
    rows: list[dict[str, Any]] = []
    hist: dict[int, int] = {k: 0 for k in WIDTHS}
    for row_index in range(count):
        if pos + 2 > len(payload):
            raise ValueError(f"truncated row {row_index}")
        if payload[pos] != 0x11:
            raise ValueError(f"row {row_index}: marker {payload[pos]:02x} != 11")
        kind = payload[pos + 1]
        width = WIDTHS.get(kind)
        if width is None or pos + width > len(payload):
            raise ValueError(f"row {row_index}: unsupported type/width {kind}")
        row = payload[pos : pos + width]
        item: dict[str, Any] = {
            "row_index": row_index,
            "offset": pos,
            "person_type": kind,
            "class": CLASS_NAMES[kind],
            "width": width,
        }
        if kind in (1, 2, 3):
            item.update(
                {
                    "ordinal": _u32(row, 71),
                    "dbid": _u32(row, 75),
                    "uid": _u32(row, 79),
                    "nation_ref": _pair(row, 2),
                    "club_ref": _pair(row, 10),
                    "world_reputation": _u16(row, 42),
                    "current_reputation": _u16(row, 44),
                    "home_reputation": _u16(row, 46),
                    "ca": _u16(row, 48),
                    "pa": _u16(row, 50),
                    "birth_year": _u16(row, 52),
                    "legacy_ca_candidate": _u16(row, 44),
                    "legacy_pa_candidate": _u16(row, 46),
                    "helper_hex": row[26:34].hex(),
                }
            )
        elif kind == 4:
            item.update(
                {
                    "ordinal": _u32(row, 22),
                    "dbid": _u32(row, 26),
                    "uid": _u32(row, 30),
                    "nation_ref": _pair(row, 2),
                    "club_ref": None,
                    "short_reputation": _u16(row, 10),
                    "birth_year": _u16(row, 12),
                    "ca": None,
                    "pa": None,
                }
            )
        else:
            item.update(
                {
                    "ordinal": _u32(row, 10),
                    "dbid": _u32(row, 14),
                    "uid": _u32(row, 18),
                    "nation_ref": None,
                    "club_ref": None,
                    "birth_year": None,
                    "ca": None,
                    "pa": None,
                }
            )
        rows.append(item)
        hist[kind] += 1
        pos += width
    chain_end = len(payload) - 9
    if pos != chain_end:
        raise ValueError(f"basic_people chain mismatch: {pos} != {chain_end}")
    stats = {
        "count": count,
        "decompressed_size": len(payload),
        "header_size": 5,
        "chain_end": pos,
        "trailer_size": 9,
        "trailer_hex": payload[-9:].hex(),
        "closure_diff": pos - chain_end,
        "widths": {str(k): v for k, v in WIDTHS.items()},
        "type_histogram": {str(k): hist[k] for k in sorted(hist)},
    }
    return rows, stats


def parse_name_table(index: int) -> tuple[dict[str, Any], list[str]]:
    fixed_path = NAME_DIR / f"payload_server_name_table_{index}.bin"
    extra_path = NAME_DIR / f"payload_server_name_table_extra_{index}.bin"
    fixed = fixed_path.read_bytes()
    extra = extra_path.read_bytes()
    if len(fixed) < 12 or len(extra) < 12:
        raise ValueError(f"name table {index}: short payload")
    n_fixed = _u32(fixed, 8)
    n_extra = _u32(extra, 8)
    fixed_end = 12 + 12 * n_fixed
    if fixed_end != len(fixed) or n_fixed != n_extra:
        raise ValueError(f"name table {index}: fixed/extra closure mismatch")
    strings: list[str] = []
    pos = 12
    utf8_errors = 0
    extra_uid_mismatches = 0
    total_utf8_bytes = 0
    for expected in range(n_extra):
        uid, length = struct.unpack_from("<II", extra, pos)
        pos += 8
        end = pos + length
        if end > len(extra):
            raise ValueError(f"name table {index}: extra record overrun")
        try:
            text = extra[pos:end].decode("utf-8")
        except UnicodeDecodeError:
            text = extra[pos:end].decode("utf-8", "replace")
            utf8_errors += 1
        if uid != expected:
            extra_uid_mismatches += 1
        strings.append(text)
        total_utf8_bytes += length
        pos = end
    if pos != len(extra):
        raise ValueError(f"name table {index}: extra closure mismatch")
    meta_a_sentinel = 0
    string_ordinal_mismatches = 0
    meta_b_min = 0xFFFF
    meta_b_max = 0
    meta_c_min = 0xFFFF
    meta_c_max = 0
    meta_d_min = 0xFFFF
    meta_d_max = 0
    for row in range(n_fixed):
        p = 12 + 12 * row
        meta_a, string_ordinal, meta_b, meta_c, meta_d = struct.unpack_from("<HIHHH", fixed, p)
        if meta_a == 0xFFFF:
            meta_a_sentinel += 1
        if string_ordinal != row:
            string_ordinal_mismatches += 1
        meta_b_min = min(meta_b_min, meta_b)
        meta_b_max = max(meta_b_max, meta_b)
        meta_c_min = min(meta_c_min, meta_c)
        meta_c_max = max(meta_c_max, meta_c)
        meta_d_min = min(meta_d_min, meta_d)
        meta_d_max = max(meta_d_max, meta_d)
    return (
        {
            "table": index,
            "fixed_file": str(fixed_path),
            "extra_file": str(extra_path),
            "count": n_fixed,
            "fixed_row_size": 12,
            "fixed_closure": len(fixed) == fixed_end,
            "extra_closure": pos == len(extra),
            "extra_record_size": "u32 uid + u32 byte_len + utf8",
            "extra_uid_mismatches": extra_uid_mismatches,
            "string_ordinal_mismatches": string_ordinal_mismatches,
            "meta_a_ffff_count": meta_a_sentinel,
            "meta_b_range": [meta_b_min, meta_b_max],
            "meta_c_range": [meta_c_min, meta_c_max],
            "meta_d_range": [meta_d_min, meta_d_max],
            "utf8_errors": utf8_errors,
            "utf8_bytes": total_utf8_bytes,
        },
        strings,
    )


def load_name_tables() -> tuple[list[dict[str, Any]], list[list[str]]]:
    stats: list[dict[str, Any]] = []
    pools: list[list[str]] = []
    for i in range(3):
        stat, pool = parse_name_table(i)
        stats.append(stat)
        pools.append(pool)
    return stats, pools


def name_join(uid: int, pools: list[list[str]]) -> dict[str, Any] | None:
    evidence = NAME_EVIDENCE.get(uid)
    if evidence is None:
        return None
    ids = {"first": evidence["first"], "second": evidence["second"], "common": evidence["common"]}
    values: dict[str, str | None] = {}
    for key, pool_index in (("first", 0), ("second", 1), ("common", 2)):
        value = ids[key]
        values[key] = None if value is None else pools[pool_index][value]
    display = values["common"] or " ".join(x for x in (values["first"], values["second"]) if x)
    return {
        "full_name": evidence["full_name"],
        "legal_name": evidence.get("legal_name"),
        "name_ids": ids,
        "name_strings": values,
        "display_from_pool": display,
        "pool_value_match": display == evidence["full_name"],
        "birth_date": evidence["birth_date"],
        "source": "people_db read chain -> name_table_extra_0/1/2",
    }


def direct_name_hits(row: dict[str, Any], payload: bytes, pools: list[list[str]]) -> list[dict[str, Any]]:
    """Check whether any aligned u32 in the basic row is a known name ordinal."""
    uid = row["uid"]
    evidence = NAME_EVIDENCE.get(uid)
    if not evidence:
        return []
    ids = {x for x in (evidence["first"], evidence["second"], evidence["common"]) if x is not None}
    raw = payload[row["offset"] : row["offset"] + row["width"]]
    hits: list[dict[str, Any]] = []
    for off in range(0, max(0, len(raw) - 3)):
        value = _u32(raw, off)
        if value in ids:
            hits.append({"wire_offset": off, "value": value})
    return hits


def person_view(row: dict[str, Any], payload: bytes, pools: list[list[str]]) -> dict[str, Any]:
    out = dict(row)
    out["offset_hex"] = f"0x{row['offset']:x}"
    join = name_join(row["uid"], pools)
    if join:
        out["name"] = join["full_name"]
        out["name_join"] = join
        out["birth_date"] = join["birth_date"]
    else:
        out["name"] = None
        out["name_join"] = None
        out["birth_date"] = None
    out["direct_basic_name_id_hits"] = direct_name_hits(row, payload, pools)
    return out


def sort_top(rows: list[dict[str, Any]], limit: int = 50) -> list[dict[str, Any]]:
    eligible = [r for r in rows if r["person_type"] in (2, 3) and r.get("ca") is not None]
    return sorted(eligible, key=lambda r: (-r["ca"], -(r.get("pa") or -1), r["uid"]))[:limit]


def anchor_view(rows_by_uid: dict[int, dict[str, Any]], payload: bytes, pools: list[list[str]]) -> list[dict[str, Any]]:
    result = []
    for uid in ANCHOR_UIDS:
        row = rows_by_uid.get(uid)
        if row is None:
            raise AssertionError(f"anchor UID missing: {uid}")
        result.append(person_view(row, payload, pools))
    return result


def make_schema(rows: list[dict[str, Any]], payload_stats: dict[str, Any], name_stats: list[dict[str, Any]], payload: bytes, pools: list[list[str]], compressed_size: int) -> dict[str, Any]:
    by_uid = {r["uid"]: r for r in rows}
    top = [person_view(r, payload, pools) for r in sort_top(rows)]
    anchors = anchor_view(by_uid, payload, pools)
    helper_probe = []
    for item in anchors:
        helper_probe.append(
            {
                "uid": item["uid"],
                "row_offset": item["offset"],
                "helper_wire_offset": 26,
                "helper_hex": item.get("helper_hex"),
                "direct_basic_name_id_hits": item["direct_basic_name_id_hits"],
                "status": "negative direct name-ID join",
            }
        )
    return {
        "schema": "fm24.t123.basic_people_l3",
        "schema_version": 1,
        "status": "byte_exact_complete; name_join_indirect_but_verified",
        "input": {
            "compressed_file": str(BASIC_PATH),
            "compressed_size": compressed_size,
            "decompression": "zstandard.ZstdDecompressor.stream_reader",
            "zstd_site_preferred": str(ZSTD_SITE),
        },
        "payload": payload_stats,
        "classes": {
            str(k): {
                "class": CLASS_NAMES[k],
                "record_width": WIDTHS[k],
                "row_count": int(payload_stats["type_histogram"][str(k)]),
                "byte_map_count": len(build_byte_map(k)),
                "byte_map": build_byte_map(k),
            }
            for k in WIDTHS
        },
        "semantic_notes": [
            "For types 1/2/3, PCAB/PPAB at row+48/+50 are the CA/PA fields from the BASIC_PERSON 4CC map.",
            "The older t115 row+44/+46 probes are retained as legacy_ca_candidate/legacy_pa_candidate and are reputation fields PCRP/PHRP.",
            "The runtime reader chooses W=4 or W=8 for the three reference reads; all 83-byte rows in this payload contain the 8-byte form.",
            "Type 4 copies its +82 value into object +80 and +84 before reading +90; those copied bytes are not duplicated on disk.",
            "The supplied source tree has no definition for sub_140FB2BA0; its +56 helper payload is therefore structurally mapped but not assigned a name 4CC.",
        ],
        "name_tables": name_stats,
        "name_join": {
            "direct_basic_row_join": "not proven; negative for all three anchors",
            "helper_va": "0x140fb2ba0",
            "helper_wire_offset": 26,
            "helper_probe": helper_probe,
            "verified_join_source": "people_db read-chain name IDs, then name_table_extra_0/1/2",
            "verified_anchor_names": {str(x["uid"]): x["name"] for x in anchors},
        },
        "anchors": anchors,
        "top50_by_PCAB": top,
    }


def check_document(doc: dict[str, Any]) -> None:
    payload = doc["payload"]
    if payload["count"] != 658011 or payload["closure_diff"] != 0:
        raise AssertionError("payload closure/count check failed")
    if payload["type_histogram"] != {"1": 166064, "2": 476158, "3": 4757, "4": 9839, "5": 1193}:
        raise AssertionError("type histogram changed")
    if [len(doc["classes"][str(k)]["byte_map"]) for k in WIDTHS] != [83, 83, 83, 34, 22]:
        raise AssertionError("byte-map coverage failed")
    anchors = {x["uid"]: x for x in doc["anchors"]}
    expected = {
        28049320: (184, 185, 184, 185, 1993, "Harry Kane"),
        735216: (160, 196, 160, 200, 1985, "Cristiano Ronaldo"),
        7458500: (185, 200, 200, 200, 1987, "Lionel Messi"),
    }
    for uid, (ca, pa, legacy_ca, legacy_pa, year, name) in expected.items():
        got = anchors[uid]
        if (got["ca"], got["pa"], got["legacy_ca_candidate"], got["legacy_pa_candidate"], got["birth_year"], got["name"]) != (ca, pa, legacy_ca, legacy_pa, year, name):
            raise AssertionError(f"anchor mismatch for {uid}: {got}")
        if not got["name_join"]["pool_value_match"]:
            raise AssertionError(f"name pool verification failed for {uid}")
    if len(doc["top50_by_PCAB"]) != 50:
        raise AssertionError("top-50 size failed")
    for row in doc["top50_by_PCAB"]:
        if not row["name"] or not row["name_join"]["pool_value_match"]:
            raise AssertionError(f"top-50 name verification failed for {row['uid']}")
    for kind in WIDTHS:
        if [x["wire_offset"] for x in doc["classes"][str(kind)]["byte_map"]] != list(range(WIDTHS[kind])):
            raise AssertionError(f"byte offset gap type {kind}")
    for stat in doc["name_tables"]:
        if not stat["fixed_closure"] or not stat["extra_closure"] or stat["extra_uid_mismatches"] or stat["string_ordinal_mismatches"]:
            raise AssertionError(f"name table closure failed: {stat['table']}")


def _date_text(value: str | None) -> str:
    return value or ""


def write_report(doc: dict[str, Any]) -> None:
    p = doc["payload"]
    lines = [
        "# t123 — basic_people_db.dat L3 decoder",
        "",
        "**Status:** byte-exact record grammar and BASIC_PERSON/PERSON byte map complete. Name resolution is verified indirectly through the people read chain and `name_table_extra_0/1/2`; the direct `basic_people` row-to-name-ID join remains negative.",
        "",
        "## Closure",
        "",
        f"The zstandard payload contains **{p['count']:,}** rows. The parser ended at `{p['chain_end']}` and `len(payload)-9` is the same value (`diff={p['closure_diff']}`). Type counts are `{p['type_histogram']}` and widths are `{p['widths']}`.",
        "",
        "## Byte Map",
        "",
        "Types 1/2/3 are 83 bytes. Their semantic sequence is `Pnti` (reference pair), `Pcti`, `Pnai`, the unresolved `sub_140FB2BA0` helper, `Pdva`, `Pcww`, `PWRP`, `PCRP`, `PHRP`, `PCAB`, `PPAB`, `Pdob`, the remaining BASIC_PERSON fields, then PERSON +24 and identity `[ordinal, dbid, uid]`.",
        "",
        "Type 4 is 34 bytes: marker/type, 8-byte `Pnti`, 2-byte `PCRP` at object +82, 2-byte `Pdob`, PERSON +24, and the 12-byte identity. The reader copies the short reputation into object +80 and +84.",
        "",
        "Type 5 is 22 bytes: marker/type, PERSON +24, and the 12-byte identity. The generated JSON contains one entry for every byte, including prefix and base-PERSON bytes.",
        "",
        "### CA/PA correction",
        "",
        "The prior t115 probes at row+44/+46 are preserved as legacy candidates. The 4CC map makes row+48/+50 the actual `PCAB`/`PPAB` values. This changes Messi from the old candidate `200/200` to semantic `185/200`, and changes Ronaldo's semantic PA to `196`; the old `160/200` probe remains visible in the anchor record.",
        "",
        "## Name Tables",
        "",
    ]
    for stat in doc["name_tables"]:
        lines.append(f"- `name_table_{stat['table']}`: {stat['count']:,} fixed 12-byte rows; extra pool closure `{stat['extra_closure']}`; UTF-8 bytes `{stat['utf8_bytes']:,}`.")
    lines += [
        "",
        "The direct row bytes do not contain any of the three anchor name ordinals, and the +56 helper definition is absent from the supplied decompilation set. The verified path is the people read-chain's three 4-byte name IDs followed by the three extra pools. The resulting anchor names are Harry Kane, Cristiano Ronaldo, and Lionel Messi.",
        "",
        "## Verified Top 50 by PCAB (CA)",
        "",
        "| # | Name | UID | Type | CA | PA | Birth date | Nation (ordinal/UID) | Club (ordinal/UID) |",
        "|---:|---|---:|---:|---:|---:|---|---|---|",
    ]
    for rank, row in enumerate(doc["top50_by_PCAB"], 1):
        nation = row.get("nation_ref")
        club = row.get("club_ref")
        ns = f"{nation['ordinal']}/{nation['uid']}" if nation else "-"
        cs = f"{club['ordinal']}/{club['uid']}" if club else "-"
        lines.append(f"| {rank} | {row['name']} | {row['uid']} | {row['person_type']} | {row['ca']} | {row['pa']} | {_date_text(row.get('birth_date'))} | {ns} | {cs} |")
    lines += [
        "",
        "The complete byte map, all anchor probes, raw helper probes, and name-pool closure statistics are in `basic_people_l3_complete.json`.",
        "",
    ]
    (OUTDIR / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def write_done(doc: dict[str, Any]) -> None:
    p = doc["payload"]
    text = "\n".join(
        [
            "DONE type=t123",
            "",
            f"- rows={p['count']} closure_diff={p['closure_diff']}",
            f"- type_histogram={json.dumps(p['type_histogram'], separators=(',', ':'))}",
            "- byte_maps=83/83/83/34/22 (every serialized byte represented)",
            "- name_tables=3 fixed+extra pools, all closures exact",
            "- verified_anchors=3 (Harry Kane, Cristiano Ronaldo, Lionel Messi)",
            "- verified_top50=50 by PCAB/CA with name-pool ID checks",
            "- --selftest=PASS",
            "",
        ]
    )
    (OUTDIR / "DONE.md").write_text(text, encoding="utf-8")


def build_outputs() -> dict[str, Any]:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    payload, compressed_size = decompress_basic()
    rows, payload_stats = parse_basic(payload)
    name_stats, pools = load_name_tables()
    doc = make_schema(rows, payload_stats, name_stats, payload, pools, compressed_size)
    check_document(doc)
    (OUTDIR / "basic_people_l3_complete.json").write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(doc)
    write_done(doc)
    return doc


def load_for_cli() -> tuple[bytes, list[dict[str, Any]], list[list[str]]]:
    payload, _ = decompress_basic()
    rows, _ = parse_basic(payload)
    _, pools = load_name_tables()
    return payload, rows, pools


def write_full_dump(payload: bytes, rows: list[dict[str, Any]], pools: list[list[str]]) -> Path:
    path = OUTDIR / "basic_people_records.jsonl"
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(person_view(row, payload, pools), ensure_ascii=False, separators=(",", ":")) + "\n")
    return path


def selftest() -> None:
    doc = build_outputs()
    check_document(doc)
    print("SELFTEST PASS")
    print(f"rows={doc['payload']['count']} closure_diff={doc['payload']['closure_diff']}")
    print(f"types={doc['payload']['type_histogram']}")
    print("byte_maps=83/83/83/34/22")
    print("anchors=3 names=Harry Kane,Cristiano Ronaldo,Lionel Messi")
    print("top50=50")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="FM24 basic_people_db L3 decoder")
    parser.add_argument("--selftest", action="store_true", help="decode, validate, and regenerate the staged outputs")
    parser.add_argument("--uid", type=int, help="print one decoded person by UID")
    parser.add_argument("--search", help="case-insensitive search over verified names")
    parser.add_argument("--top", nargs="?", const=50, type=int, help="print top N players by semantic PCAB/CA")
    parser.add_argument("--dump", action="store_true", help="write complete decoded rows to basic_people_records.jsonl")
    args = parser.parse_args(argv)
    if args.selftest:
        selftest()
        return 0
    if args.uid is not None or args.search is not None or args.top is not None or args.dump:
        payload, rows, pools = load_for_cli()
        if args.uid is not None:
            row = next((r for r in rows if r["uid"] == args.uid), None)
            if row is None:
                print(json.dumps({"error": "UID not found", "uid": args.uid}))
                return 1
            print(json.dumps(person_view(row, payload, pools), ensure_ascii=False, indent=2))
        elif args.search is not None:
            needle = args.search.casefold()
            found = []
            for row in rows:
                view = person_view(row, payload, pools)
                if view.get("name") and needle in view["name"].casefold():
                    found.append(view)
            print(json.dumps(found, ensure_ascii=False, indent=2))
        elif args.top is not None:
            top = [person_view(r, payload, pools) for r in sort_top(rows, args.top)]
            print(json.dumps(top, ensure_ascii=False, indent=2))
        elif args.dump:
            path = write_full_dump(payload, rows, pools)
            print(str(path))
        return 0
    doc = build_outputs()
    print("t123 outputs written")
    print(f"rows={doc['payload']['count']} closure_diff={doc['payload']['closure_diff']}")
    print(f"types={doc['payload']['type_histogram']}")
    print("byte_maps=83/83/83/34/22")
    print("name_tables=3 exact fixed/extra closures")
    print("anchors=3 verified; top50=50")
    print(f"outdir={OUTDIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
