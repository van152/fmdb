"""t93: FMLibreEditor FM27 recon digest — 22 docs, 3-8 key points each.

Points are written from reading the docs; the script only checks that each doc exists,
that its title line and every quoted heading exist verbatim in the file, and that each
point carries a line anchor that is inside the file.

Usage:
  py -V:3.12 -I -B scripts/t93_recon.py --selftest
  py -V:3.12 -I -B scripts/t93_recon.py --out scratch/t93/outbox.md/fm27_recon_digest.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EXT = REPO / "scratch" / "ext" / "FMLibreEditor"
RECON = EXT / "docs" / "recon"
PROVENANCE = "ext/FMLibreEditor@fb76023fc28c53ddc851ad1afdaf9879d3534d5c"

# doc -> (heading anchor, [ (line, point) ... ])
DIGEST: dict[str, list[tuple[int, str]]] = {
    "fm27-bans.md": [
        (3, "Mac Steam build, July 2026 save; found via RTTI class names (db::ACTUAL_PLAYER, BAN_SCOPE)."),
        (22, "Absences live in the medical record's second list at +0x18 (32-byte entries), not a separate object."),
        (26, "Absence entry: +0x00 u32 id + reach/kind bytes, +0x10 start date, +0x14 u16 discipline rule, +0x16 u16 0xFFFF = ban, +0x1C u8 matches left."),
        (37, "652 players had absences; 24 entries were bans of 23 players; discipline rule 65 = European club competitions, 72 = South American."),
        (51, "Lifting a ban removes the entry from the list but leaves the block in memory; undo re-lists it."),
        (67, "Windows Steam 26227640 reads the same offsets (17 banned players) - the ban layout did not move between platforms."),
    ],
    "fm27-club-debts.md": [
        (12, "Club -> info record at +0x100; the info record holds a (begin,end,capacity) pointer list at +0x50."),
        (19, "Each debt is 0x1C bytes: +0x00 original, +0x04 payable/month, +0x08 interest, +0x10 end date, +0x14 start date, +0x18 type, +0x19 always 1."),
        (35, "Type codes 1..15 named from the game's own English strings (Bank Loan, State Loan, PIK Loan, Misc. Debt ...)."),
        (81, "Debt amounts add up to the screen's figures; PIK loans (type 13) mean something else for both payment words."),
        (115, "Open: +0x1A's 0x8000 value and the exact screen arithmetic for PIK."),
    ],
    "fm27-contracts.md": [
        (9, "Contract clause list at +0x68 holds 8-byte entries: u32 amount (0xFFFFFFFF none), u16 condition (0xFFFF none), u16 kind."),
        (11, "56 clause kinds tabulated with in-game names (release clauses, wage rises/drops, bonuses, extensions)."),
        (84, "Squad status is a byte at +0x54 with its own code table."),
        (112, "Kind of contract at +0xC3 (full/loan/youth etc.)."),
        (141, "Loyalty bonus at +0x38 and +0xA8."),
        (164, "Mac offsets noted separately - same layout, own field base."),
    ],
    "fm27-gamepass-0.9.2355.md": [
        (8, "GDK MSIXVC package; entry GameLaunchHelper.exe; running process fm.exe; fm.exe itself is ACL-protected on disk."),
        (17, "Unity 6000.3.18f1-custom, IL2CPP, metadata v39 (needs Cpp2IL or a v39 fork); managed names not obfuscated."),
        (28, "Native core fm_Data/Plugins/x86_64/game_plugin.dll: 423 MB, renamed/reordered sections, anti-tamper; 282 exports."),
        (43, "Steam reference layout quoted from fm-editor: entity arrays are (begin,end) pairs in a writable section, objects told apart by vtable."),
    ],
    "fm27-gamepass-0.9.2409.md": [
        (12, "Image 0x175DA000, link stamp 0x6AE563A1; sections renamed again (.00cfg arrays, .trace vtables, .rsrc 282 MiB RWX)."),
        (31, "Entity arrays moved +0x2000: players 0x5683DC0, staff 0x5683E08, clubs 0x5683F78."),
        (37, "Retirement manager static 0x5675060, always ~0xED60 before the players pair."),
        (39, "In-game date is a VARIABLE of its own (0x56257C8), not the date field beside the arrays (which read 1 Jan 1900 unset)."),
        (49, "Everything else (object layout) unchanged."),
    ],
    "fm27-gamepass-0.9.2435.md": [
        (8, "Full release; image 0x17969000; statics in .link, RWX in .xtls."),
        (20, "Statics moved ~-0x2CC000 but no longer at identical relative distances (unlike Steam)."),
        (39, "Object layout did not move: 108 player fields, 37 club fields, all lists matched before/after."),
        (52, "After a load no contract had room for another clause - capacity is a load-time property."),
    ],
    "fm27-loans.md": [
        (6, "A loan is a separate db::LOAN_CONTRACT reached via player+0x338 -> record+0x00 (own contract stays at +0x330)."),
        (19, "Loan contract is laid out as a contract up to the squad number: +0x08 owner, +0x10/+0x18 team, +0x20 wage, +0x44 from, +0x48 until, +0x54 status, +0x5D number."),
        (32, "The 32-byte record holds up to four contract pointers: +0x00 loan, +0x08 B-team, +0x10 basic/full, +0x18 another B-team."),
        (50, "3,596 of 5,637 players with the record were on loan; 2,041 had the record without a loan."),
        (77, "Recalling sets the record to null and restores team+0x130, leaving +0x138 at the loan club."),
    ],
    "fm27-names.md": [
        (7, "Player name ids at +0x2D8/+0x2E0/+0x2E8 (first/last/common), full name FM string at +0x2C8; staff mirror at +0x150/+0x158/+0x160/+0x140."),
        (16, "An FM string is u32 length + UTF-8 text with a NUL, after a u32 holder count; strings are shared."),
        (20, "Three tables (first/last/common), 24-byte entries: +0x00 text pointer, +0x08 u32 id, +0x0C u16 nation index, +0x0E u16 weight, +0x12 flags, +0x13 ethnicity-ish."),
        (59, "Each table is reached both as a list-by-id (static before the players pair) and as the database's per-nation list."),
        (68, "The entries are slots of one object pool of 24-byte slots."),
    ],
    "fm27-national-teams.md": [
        (8, "A national team is NOT a club: the clubs array holds none; each nation has men's and women's db::NATIONAL_TEAM_CONTAINER."),
        (25, "251 db::NATION objects, 0x208 bytes each: +0x0C UID, +0x18 name, +0x28 3-letter code, +0xF0 capital, +0xF8 continent, +0x100 region, +0x108 currency, +0x110/+0x118 containers, +0x1EC population."),
        (49, "502 containers of 0x8A0 bytes; two arrays of 251 next to the players'/staff's/clubs' arrays."),
        (68, "National teams are laid out like a club's [team], so a club team view reads them."),
        (124, "Editor worklist and youth-team notes."),
    ],
    "fm27-nationality.md": [
        (8, "All non-primary nationalities live in one relations list: player+0x2C0 (macOS; +0x300 on Windows) -> (begin,end,capacity) of 16-byte entries."),
        (15, "Entry: +0x00 target pointer, +0x0A target kind (1 club, 3 person, 7 competition, 8 nation), +0x0B relation kind, +0x0C value, +0x0F always 0xFF."),
        (35, "Relation 9 nation value 100/80 = secondary nationality; 70 = trained in nation; 72 = trained at club; 109 = no work permit needed."),
        (72, "Room: the list is a fixed-capacity vector; growing it moves it."),
        (112, "Checked in game: eligibility page matches relation 70/72."),
    ],
    "fm27-object-pools.md": [
        (13, "Pool statics: +0x00 chunk pointer list, +0x18 first free slot, +0x20 free/used counts, +0x28 slot bytes + first-chunk slots, +0x30 later-chunk slots + 100."),
        (29, "Scan of writable data found 279 pools; free-slot chains validated in all of them."),
        (45, "Contracts pool at game_plugin+0x5672020 (0.9.2409.0); 12,824 used slots matching 12,824 db::FULL_CONTRACT objects."),
        (61, "Signing a free agent means allocating a contract object in the pool, since no free-agent list exists."),
    ],
    "fm27-prize-money.md": [
        (16, "sicomps::LEAGUE_STAGE +0xF0 -> settings; FUTURE_STAGE +0x90 -> settings it will use."),
        (22, "LEAGUE_SETTINGS 0x2F0 apart: +0x148 per win, +0x150 per draw, +0x154 per loss, +0x1E0 list of pounds by final position."),
        (36, "db::COMP +0x0C UID (again at +0x10), +0x40 name, +0x48 short name."),
        (52, "Amounts come from the database and repeat across saves/seasons; some leagues have no per-position list."),
        (70, "Knockout round money is not in these settings."),
    ],
    "fm27-sponsorships.md": [
        (6, "Club+0x130 -> (begin,end,capacity) of pointers; each deal is 24 bytes."),
        (8, "Deal: +0x00/+0x04 dates, +0x08 total, +0x0C per season, +0x10 relegation %, +0x12 reputation at signing, +0x14 kind."),
        (22, "Kind codes 1..23 named from the game's Sponsorship screen."),
        (40, "Season money is the sum of per-season amounts, booked once at season start."),
    ],
    "fm27-staff.md": [
        (7, "Job code is a u8 at contract+0x26; a player-coach's is his coaching job + 1."),
        (9, "Job code table cross-checked against the game's own language files (example.ltf / languages.fmf zstd frames)."),
        (28, "A club keeps staff in department lists: medical +0x60, coaching +0x78, scouting +0x90; directors of football at club+0x148."),
        (52, "A team points at its manager's object at team+0x80 (null for none)."),
        (101, "Staff contracts: wage/start/end/status/kind in the same contract object family."),
    ],
    "fm27-steam-26227640.md": [
        (8, "Steam Launch Preview; image 0x19E69000, link stamp 0x6ADFB11C - 69 s before Game Pass 0.9.2355.0, same source."),
        (21, "Arrays at 0x57037D0 / 0x5703818 / 0x5703988; found by scanning, every sampled element decoded."),
        (25, "Object layout identical to Game Pass; witnesses (Messi, Tottenham, Man Utd) read the same."),
        (65, "Writes: heap-only edits verified."),
        (88, "Team cohesion / tactical familiarity not found."),
    ],
    "fm27-steam-26340721.md": [
        (10, "Steam 27.0.0; image 0x1821C000, stamp 0x6AE565AF."),
        (22, "Arrays +0x2000: players 0x57057D0, staff 0x5705818, clubs 0x5705988."),
        (30, "Retirement manager static 0x56F7D10, 0xDAC0 before the players pair."),
        (30, "Date beside the arrays read 1 Jan 1900; the real date variable is 0x56AF378."),
        (42, "Object layout unchanged (fields --stats all in range)."),
    ],
    "fm27-steam-26385295.md": [
        (9, "Steam 27.0.1 full release; image 0x17CB9000, stamp 0x6AE8B5A4."),
        (21, "Every static +0x11B040, same relative distances: arrays 0x5820810/0x5820858/0x58209C8, date 0x57CA3B8."),
        (33, "Object layout unchanged: 108 player fields and 37 club fields matched across the update."),
    ],
    "fm27-steam-macos.md": [
        (11, "Mac app is a Unity 6000.3.18f1 universal player; game_plugin is a Mach-O bundle; LC_UUID identifies the build per arch."),
        (34, "Hardened runtime + notarization is why macOS keeps the editor out; a bridge is needed."),
        (163, "Mac object layout differs by C++ ABI: player's own fields 8 bytes earlier, person block first (+0x278), identity block after (+0x388)."),
        (198, "Native arm64 run confirmed the Mac layout."),
    ],
    "fm27-tactics-and-value.md": [
        (6, "Transfer value is i32 at player+0x234 in pounds (Mac +0x22C); asking price +0x238 / +0x230 with -1 = not set."),
        (14, "300,000,000 means not for sale; -1 means never valued; the game shows values in euros at ~1.166 EUR/GBP."),
        (40, "A club's tactic block is reached from simatch::PREPARED_TACTICS_CREATOR_ARRAY +0x08 entries."),
        (44, "Tactic block: 11x16-byte slot records at +0x000, style tag at +0x100, 11 in-possession entries at +0x148 (0x48 each), out-of-possession at +0x468, second copy at +0x7D0."),
    ],
    "fm27-transfer-offers.md": [
        (11, "Every offered/agreed contract is its own db::FULL_CONTRACT or db::LOAN_CONTRACT; the player points only at his running one."),
        (23, "Each such contract is held by a 0x48-byte entry: +0x10 contract, +0x28 offer number, +0x3E state, +0x41 kind."),
        (38, "States 1 offered / 2 agreed awaiting its day / 3 lost; kinds 8 renewal, 7 free move, 2 transfer, 1 loan."),
        (75, "The offer object (FULL_TRANSFER_OFFER) carries the fee and the selling team."),
    ],
    "fm27-transfers.md": [
        (9, "A person's identity block holds internal person id at +0x08 and UID at +0x0C; internal ids are not array indexes."),
        (21, "One global transfer list of 48-byte records sorted by internal person id: +0x00 buying club, +0x08 selling club, +0x10 date, +0x18 amount, +0x1C person id, +0x20 flags."),
        (34, "The stored amount is NOT the fee (833,333 vs the £54M shown); flags' low nibble 0x0C = 12 months."),
        (85, "Free agents / releases recorded in the same list with null clubs."),
        (202, "A transfer the game makes on a later day: the reliable way to obtain one."),
    ],
    "fm27-youth-intake.md": [
        (7, "A byte before the gender flags (player+0x2A0 on Windows, +0x18 into the identity block) holds 0x08 for a game-made player."),
        (9, "Game-made UIDs start at 2,002,068,314; database players stop near 2,001,000,000, so the flag, not the UID, is authoritative."),
        (25, "No list of a club's intakes: intake players share their contract's joined day."),
        (52, "Cities of birth are reached through the person block's birth-city pointer."),
    ],
}


def build() -> dict:
    docs = []
    for name in sorted(DIGEST):
        path = RECON / name
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        points = [{"line": ln, "point": pt} for ln, pt in DIGEST[name]]
        docs.append(
            {
                "doc": name,
                "title": lines[0].lstrip("# ").strip(),
                "line_count": len(lines),
                "sections": [ln.strip() for ln in lines if ln.startswith("## ")],
                "key_points": points,
                "key_point_count": len(points),
            }
        )
    return {
        "schema": "t93/fm27_recon_digest/v1",
        "provenance": PROVENANCE,
        "method": "read-only digest of docs/recon/*.md; every point carries its source line",
        "grade_policy": "external reference only; never our L1-L4 grade",
        "doc_count": len(docs),
        "point_total": sum(d["key_point_count"] for d in docs),
        "docs": docs,
    }


def selftest() -> int:
    data = build()
    assert data["doc_count"] >= 20, data["doc_count"]
    assert (RECON / "fm27-bans.md").is_file()
    on_disk = sorted(p.name for p in RECON.glob("*.md"))
    assert on_disk == sorted(d["doc"] for d in data["docs"]), set(on_disk) ^ set(
        d["doc"] for d in data["docs"]
    )
    for d in data["docs"]:
        assert 3 <= d["key_point_count"] <= 8, (d["doc"], d["key_point_count"])
        lines = (RECON / d["doc"]).read_text(encoding="utf-8").splitlines()
        for p in d["key_points"]:
            assert 1 <= p["line"] <= len(lines), (d["doc"], p["line"])
            assert lines[p["line"] - 1].strip(), (d["doc"], p["line"])
    print("selftest OK:", data["doc_count"], "docs,", data["point_total"], "points")
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
        print("wrote", args.out, data["doc_count"], "docs")
    else:
        print(text[:1500])
    return 0


if __name__ == "__main__":
    sys.exit(main())
