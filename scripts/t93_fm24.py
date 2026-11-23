"""t93: parse fm-editor FM24 Rust field tables into JSON by READING them.

Never builds or runs the Rust crate. Regex-extracts `Field { ... }` and `SubRecord { ... }`
literals plus the entity-array addresses from src/fields/fm24/*.rs and mod.rs.

Usage:
  py -V:3.12 -I -B scripts/t93_fm24.py --selftest
  py -V:3.12 -I -B scripts/t93_fm24.py --out scratch/t93/outbox.md/fm24_memory_layout.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EXT = REPO / "scratch" / "ext" / "fm-editor"
PROVENANCE = "ext/fm-editor@ba605f4b64137dfc18940a69ecb2f523007f3ea8"

FIELD_RE = re.compile(
    r'Field \{ key: "(\w+)",\s*label: "([^"]*)",\s*entity: (\w+),'
    r'\s*category: (\w+),\s*offset: (None|\w+\([^)]*\))',
    re.S,
)
SUB_RE = re.compile(
    r'SubRecord \{ id: "(\w+)",\s*parent: SubRecordParent::([\w"]+\([^)]*\)|\w+),'
    r'\s*ptr_offset:\s*(0x[0-9A-Fa-f]+),\s*size:\s*(0x[0-9A-Fa-f]+)\s*\}',
    re.S,
)


def parse(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    fields, subs = [], []
    for m in FIELD_RE.finditer(text):
        line = text.count("\n", 0, m.start()) + 1
        fields.append(
            {
                "key": m.group(1),
                "label": m.group(2),
                "entity": m.group(3),
                "category": m.group(4),
                "offset_expr": m.group(5),
                "located": m.group(5) != "None",
                "file": path.relative_to(EXT).as_posix(),
                "line": line,
            }
        )
    for m in SUB_RE.finditer(text):
        line = text.count("\n", 0, m.start()) + 1
        subs.append(
            {
                "id": m.group(1),
                "parent": m.group(2),
                "ptr_offset": m.group(3),
                "size": m.group(4),
                "file": path.relative_to(EXT).as_posix(),
                "line": line,
            }
        )
    return {"fields": fields, "sub_records": subs}


CURATED = [
    {
        "id": "M01_module",
        "statement": "FM24 has no game_plugin.dll: game logic and every entity-array RVA live in fm.exe itself (image base 0x140000000), so gp_base is the fm.exe base.",
        "file": "docs/fm24/memory-layout.md",
        "line": 9,
    },
    {
        "id": "M02_players_array",
        "statement": "Player entity array: std::vector of object pointers at fm.exe+0x642EDD0 (data) / +0x642EDD8 (end), 83,426 entries, vtable fm.exe+0x5A4E958, pool stride 0x3E8.",
        "file": "docs/fm24/memory-layout.md",
        "line": 32,
    },
    {
        "id": "M03_staff_array",
        "statement": "Staff entity array at fm.exe+0x642EDE8 / +0x642EDF0, 33,835 entries (human manager last), vtable fm.exe+0x5A4C2E8, stride 0x268.",
        "file": "docs/fm24/memory-layout.md",
        "line": 33,
    },
    {
        "id": "M04_clubs_array",
        "statement": "Club entity array at fm.exe+0x642EF58 / +0x642EF60, 36,725 entries, vtable fm.exe+0x5A51F38, 0x170 spacing between objects.",
        "file": "docs/fm24/memory-layout.md",
        "line": 34,
    },
    {
        "id": "M05_array_scan_method",
        "statement": "Arrays were found by scanning fm.exe's writable sections for (data,end) pointer pairs, then locating witness records in the heap (Guardiola by personality bytes, Kane by UID) and finding which arrays point at them.",
        "file": "docs/fm24/memory-layout.md",
        "line": 36,
    },
    {
        "id": "M06_stadium_root",
        "statement": "The stadium array root is NOT located; stadiums are reached per club through the home_stadium sub-record, so rva_stadium_base = 0. Stadium entity stride is 0xB0.",
        "file": "docs/fm24/memory-layout.md",
        "line": 45,
    },
    {
        "id": "M07_current_date",
        "statement": "Current game date is the static DateDayYear at fm.exe+0x631D5BC: day-of-year in the low 9 bits, FM flag bits above bit 8, then the year.",
        "file": "docs/fm24/memory-layout.md",
        "line": 50,
    },
    {
        "id": "M08_player_block_shift",
        "statement": "Player positions+attributes keep the FM26 order shifted +0xB8: positions 0x208..0x216, attributes 0x217..0x24C.",
        "file": "docs/fm24/memory-layout.md",
        "line": 68,
    },
    {
        "id": "M09_player_identity_offsets",
        "statement": "Individually moved player fields: home/current/world rep 0x1FA/0x1FC/0x1FE, CA/PA 0x200/0x202, height 0x14E, UID 0x284, name FmString 0x2C0, name subs 0x2D0/0x2D8, DOB 0x2BC, personality 0x2F0..0x2F7, club ptr 0x3B0.",
        "file": "docs/fm24/memory-layout.md",
        "line": 70,
    },
    {
        "id": "M10_name_split",
        "statement": "Names: 40% of players carry a direct FmString, 59% first/last sub-records, 0.5% neither.",
        "file": "docs/fm24/memory-layout.md",
        "line": 73,
    },
    {
        "id": "M11_intl_record",
        "statement": "International record: four u8 at 0x3DC..0x3DF = caps, U21 caps, goals, U21 goals (FM27 widens caps and goals to u16).",
        "file": "docs/fm24/memory-layout.md",
        "line": 77,
    },
    {
        "id": "M12_player_nation_city_team",
        "statement": "Nation pointer 0x2E8 (name FmString at nation+0x18); birth city pointer 0x300 (name at city+0x18); team pointer 0x130 with club at team+0x30.",
        "file": "docs/fm24/memory-layout.md",
        "line": 80,
    },
    {
        "id": "M13_contract_object",
        "statement": "Contract pointer 0x340: wage i32 GBP/week at +0x18, expiry at +0x40, squad status +0x4C, squad number +0x55, contract start (FM27 signed) +0x3C, listing flags +0x4F (bit0 transfer, bit1 loan), listed date +0x48, listing code +0x50.",
        "file": "docs/fm24/memory-layout.md",
        "line": 86,
    },
    {
        "id": "M14_weight_traits_morale",
        "statement": "Weight u16 kg at 0x14C; traits (PPMs) u64 bitmask at 0x368 with bit = PPM ID - 1; morale level u8 1..20 at 0x25F.",
        "file": "docs/fm24/memory-layout.md",
        "line": 92,
    },
    {
        "id": "M15_condition_leads",
        "statement": "Condition leads read but unconfirmed: sharpness u16 0x1F4, jadedness i16 0x1F6, condition u16 0x1F8, looks 0x309..0x30C.",
        "file": "docs/fm24/memory-layout.md",
        "line": 117,
    },
    {
        "id": "M16_value_asking",
        "statement": "Transfer value i32 at 0x1D0 (FM24 recalculates it daily, so read-only); asking price i32 at 0x1D4 with -1 = Unspecified.",
        "file": "docs/fm24/memory-layout.md",
        "line": 138,
    },
    {
        "id": "M17_staff_attributes",
        "statement": "Staff attribute block (< 0x50) is the FM26 layout +8; Judging Staff Ability 0x4A, Analysing Data 0x44, Sports Science 0x47 are encoded with displayed = (raw+2)/5.",
        "file": "docs/fm24/memory-layout.md",
        "line": 166,
    },
    {
        "id": "M18_staff_identity",
        "statement": "Staff reps 0xD0/0xD2/0xD4, CA/PA 0xD6/0xD8 (4 earlier than FM26), staff ID 0x104, name 0x140, name subs 0x150/0x158, DOB 0x13C, personality 0x170, role-ratings ptr 0x1F8.",
        "file": "docs/fm24/memory-layout.md",
        "line": 175,
    },
    {
        "id": "M19_staff_employment",
        "statement": "Staff current club chain (read-only): staff+0x1C0 -> employment -> +0x10 team -> +0x30 club -> full name FmString +0xC0. FM26 keeps this pointer at +0x1A8.",
        "file": "docs/fm24/memory-layout.md",
        "line": 178,
    },
    {
        "id": "M20_human_manager",
        "statement": "Human manager is the LAST staff-array entry (vtable fm.exe+0x5A6A318) with identity fields at offset+0x358 (FM26 0x350); the direct name FmString is null in both slots on FM24.",
        "file": "docs/fm24/memory-layout.md",
        "line": 195,
    },
    {
        "id": "M21_club_top",
        "statement": "Club top level: UID 0x0C, full name 0xC0, short name 0xC8, array index 0x08.",
        "file": "docs/fm24/memory-layout.md",
        "line": 205,
    },
    {
        "id": "M22_club_info_subrecord",
        "statement": "Club info sub-record (ptr +0x100) is the FM26 layout +8: abbreviations 0x00/0x08/0x10, season tickets 0xC0, founded 0xD8, owner status 0xDE, social 0xF8, supporter % 0x106..0x10B, supporter attributes 0x114..0x119, facilities 0x120..0x12D (training 0x120, youth 0x12B).",
        "file": "docs/fm24/memory-layout.md",
        "line": 206,
    },
    {
        "id": "M23_club_finance",
        "statement": "Club finance sub-record ptr +0x150: transfer budget finance+0x7CC (i32), wage budget finance+0x810, wage spend +0x81C, next-season min transfer budget +0x7D4; the budget sub-record copies (+0x04/+0x0C) go stale.",
        "file": "docs/fm24/memory-layout.md",
        "line": 220,
    },
    {
        "id": "M24_club_stadium_chain",
        "statement": "Home stadium chain: club+0x18 -> [0] senior team -> +0x78 stadium entity; attendance figures at stadium-sub +0xB0 area and 0x68/0x6C/0x70.",
        "file": "docs/fm24/memory-layout.md",
        "line": 234,
    },
    {
        "id": "M25_stadium_fields",
        "statement": "Stadium entity (stride 0xB0): UID 0x0C, name 0x38, alt name 0x40, capacity/seated/used/all-seater/expansion u32 0x6C/0x70/0x74/0x78/0x7C, owner club ptr 0x80, pitch length/width x10 0x88/0x8A.",
        "file": "docs/fm24/memory-layout.md",
        "line": 239,
    },
    {
        "id": "M26_medical_object",
        "statement": "Medical pointer player+0xF8: injuries vector +0x00 of pointers to 0x38-byte entries (type ptr +0x08, name FmString at type+0x20, start +0x20, u16 durations +0x28/+0x2A); absences vector +0x18 of pointers to 0x20-byte entries (kind +0x05, start +0x10, u16 days +0x16; 0x19 ban, 0x1F holiday). Null medical pointer = no medical history (~96% of players).",
        "file": "docs/fm24/memory-layout.md",
        "line": 251,
    },
    {
        "id": "M27_ties_clauses",
        "statement": "Ties pointer player+0x2F8 (FM27 +0x300), 16-byte entries; clauses vector contract+0x60 (FM27 +0x68), 8-byte entries; relegation wage drop is clause type 0x0F on FM24 (0x05 on FM27).",
        "file": "docs/fm24/memory-layout.md",
        "line": 275,
    },
    {
        "id": "M28_version_gate",
        "statement": "Version gate is a RecordedBuild fingerprint = hash of the first 64 KB of fm.exe: FM24_STEAM 0xFB39952A20287907, FM24_EPIC 0x8FA113DB9DCD8883.",
        "file": "docs/fm24/memory-layout.md",
        "line": 18,
    },
    {
        "id": "M29_layout_consts",
        "statement": "ReleaseLayout constants: player_struct_size 0x3E8, staff_struct_size 0x268, club_read_size 0x200, stadium_entity_stride 0xB0, human_manager_shift set by staff module.",
        "file": "src/fields/fm24/mod.rs",
        "line": 39,
    },
    {
        "id": "M30_module_addresses",
        "statement": "ModuleAddresses for FM24_STEAM: humans 0x642EDD0/0x642EDD8, staff 0x642EDE8/0x642EDF0, clubs 0x642EF58/0x642EF60, stadium base 0, current date 0x631D5BC.",
        "file": "src/fields/fm24/mod.rs",
        "line": 72,
    },
]

MEMORY_NOTE = (
    "This is LIVE PROCESS MEMORY layout, not the save-file wire format. fm-editor reads and "
    "writes the running game's heap through the OS; offsets here are object-relative and "
    "meaningless for .dat wire parsing. Do not map these offsets onto wire slots."
)


def build() -> dict:
    out = {"fields": [], "sub_records": []}
    files = sorted((EXT / "src/fields/fm24").glob("*.rs"))
    for path in files:
        got = parse(path)
        out["fields"].extend(got["fields"])
        out["sub_records"].extend(got["sub_records"])
    by_entity: dict[str, dict] = {}
    for f in out["fields"]:
        e = by_entity.setdefault(f["entity"], {"total": 0, "located": 0, "unlocated": 0})
        e["total"] += 1
        e["located" if f["located"] else "unlocated"] += 1
    out["entity_counts"] = by_entity
    out["file_count"] = len(files)
    out["provenance"] = PROVENANCE
    out["schema"] = "t93/fm24_memory_layout/v1"
    out["domain"] = "live process memory (fm.exe image base 0x140000000)"
    out["domain_note"] = MEMORY_NOTE
    out["method"] = (
        "regex parse of src/fields/fm24/*.rs plus curated facts from "
        "docs/fm24/memory-layout.md; nothing built or executed"
    )
    out["grade_policy"] = "external reference only; never our L1-L4 grade"
    out["curated_facts"] = CURATED
    out["memory_layout_is_not_wire"] = True
    return out


def selftest() -> int:
    data = build()
    assert data["file_count"] >= 5, data["file_count"]
    assert len(data["fields"]) >= 150, len(data["fields"])
    assert len(data["sub_records"]) >= 10, len(data["sub_records"])
    for ent in ("Player", "Staff", "Club", "Stadium"):
        assert ent in data["entity_counts"], ent
    keys = {f["key"] for f in data["fields"]}
    for k in ("p_uid", "s_ca", "c_uid", "st_capacity"):
        assert k in keys, k
    for f in data["fields"]:
        assert (EXT / f["file"]).is_file(), f["file"]
    assert len(data["curated_facts"]) >= 25
    doc = EXT / "docs/fm24/memory-layout.md"
    for fact in data["curated_facts"]:
        assert (EXT / fact["file"]).is_file(), fact["file"]
        if fact["file"].startswith("docs/"):
            assert fact["line"] <= len(doc.read_text(encoding="utf-8").splitlines())
    print(
        "selftest OK:",
        len(data["fields"]),
        "fields,",
        len(data["sub_records"]),
        "sub-records,",
        len(data["curated_facts"]),
        "facts",
    )
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=None)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    data = build()
    text = json.dumps(data, ensure_ascii=False, indent=1) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print("wrote", args.out, len(data["fields"]), "fields")
    else:
        print(text[:2000])
    return 0


if __name__ == "__main__":
    sys.exit(main())
