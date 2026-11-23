"""t93 step 6 -- crosswalk of our frozen assets against the three external corpora.

Read-only over both sides: nothing here executes or imports external code, and no external
label ever upgrades our grading. Every entry ships verdict=held.

    py -V:3.12 -I -B scripts/t93_crosswalk.py --selftest
    py -V:3.12 -I -B scripts/t93_crosswalk.py --out scratch/t93/outbox.md/crosswalk.json
"""

from __future__ import annotations

import json
import sys

FMSAVE = "ext/fmsave@755fe9c"
FMEDIT = "ext/fm-editor@ba605f4"
FMLIBRE = "ext/FMLibreEditor@fb76023"

PROV = {
    "ext/fmsave": {
        "commit": "755fe9c566bb0497d4ad6ef6e1ac1fd2fde7351b",
        "license": "MIT",
        "role": "FM26/27 save-file wire grammar (sections, records, zstd frames)",
    },
    "ext/fm-editor": {
        "commit": "ba605f4b64137dfc18940a69ecb2f523007f3ea8",
        "license": "GPL",
        "role": "FM24/26/27 live process memory layout (RVAs, strides, member offsets)",
    },
    "ext/FMLibreEditor": {
        "commit": "fb76023fc28c53ddc851ad1afdaf9879d3534d5c",
        "license": "GPL",
        "role": "FM27 recon notes (object pools, contracts, transfers, names)",
    },
}

INTERNAL = {
    "scratch/t92/out/schema_v113.json": "e4175578d587e201b7d0b14bd15c69c967679049d4a0d236cd4f9e861944254e",
    "scratch/t88/out3/slots.json": "f1050953d19da7ea30902f3cc11ee4eb0cf1e55b1f4ca8be408f7f2026663420",
    "reports/stage2_table_identity.json": "f2533a06de4e79c19b26d93c4f51471da7c0552d45a0c20b54ccc31c4f5b14c7",
}

POLICY = {
    "verdict_vocabulary": "held (this file uses no other value)",
    "rule": (
        "An external corpus can point at a place to look; it cannot raise, lower or confirm our "
        "L1-L4 grade. Every entry below is held even where the two sides agree exactly, and an "
        "agreement between two external repos is still external-only evidence."
    ),
    "domains_kept_apart": (
        "fmsave describes save-file wire bytes; fm-editor and FMLibreEditor describe live process "
        "memory of a running game. A byte match across those domains is a coincidence of "
        "concept, never a transfer of evidence."
    ),
}


def X(id, topic, ours, ext, relation, why, residual):
    """One crosswalk row. `ours` = (artifact#pointer, grade, statement)."""
    return {
        "id": id,
        "topic": topic,
        "our_side": {"artifact": ours[0], "grade": ours[1], "statement": ours[2]},
        "external_side": [
            {"provenance": p, "locator": loc, "statement": st, "ext_label": lab}
            for (p, loc, st, lab) in ext
        ],
        "relation": relation,
        "verdict": "held",
        "why_not_upgraded": why,
        "residual": residual,
    }


ITEMS = [
    X(
        "X01",
        "table_9.dat header framing vs the fmsave section head",
        (
            "scratch/t92/out/schema_v113.json#/table9_closure_e127/chains/client|table_9.dat/framing",
            "L2",
            "client_db/table_9.dat opens 03 01 74 61 64 2e f1 0d fb 00 00 00 00 (13-byte header: "
            "magic 03 01, reversed extension 'dat.', u16 schema, u32 row count 251, zero byte).",
        ),
        [
            (
                FMSAVE,
                "src/fmsave/_version.py:54,56,88",
                "SECTION_MAGIC_PREFIX = b'\\x03\\x01'; SCHEMA_OFFSET = 6; a section head is the "
                "prefix plus the reversed extension, and the u16 at offset 6 is its schema.",
                "grammar",
            )
        ],
        "structural_match",
        "fmsave reads sections of a save container (game_db, humans, tactics_man...). Our "
        "table_9.dat is a database-table payload inside a client archive; the shared 13/8-byte "
        "head shape does not make the tables the same table, and fmsave never reads table_9.",
        "Bytes 6-7 of our header decode as 0x0DF1 under fmsave's SCHEMA_OFFSET rule; what that "
        "number means for a client_db table stays unproven on our side.",
    ),
    X(
        "X02",
        "record closing header: <III vs our 12-byte trailer and 13-byte identity",
        (
            "scratch/t92/out/schema_v113.json#/table45_structure_e132_e138/row_decomposition_e138",
            "L2",
            "table_45 rows end with a 12-byte identity [ordinal u32][uid u32][uid u32] plus a u8 "
            "tail 0; table_9 rows carry a 12-byte trailer; both are fixed distance from row end.",
        ),
        [
            (
                FMSAVE,
                "src/fmsave/readers/nations.py:30",
                "_CLOSING_HEADER = struct.Struct('<III'): row position, database id, a third word.",
                "grammar",
            ),
            (
                FMSAVE,
                "src/fmsave/readers/club_table.py:11,100",
                "_FOOTER = struct.Struct('<III'); a row's footer must hold its own ordinal.",
                "grammar",
            ),
        ],
        "structural_match",
        "Same width and same ordinal-first discipline, different payload: fmsave's second word is "
        "a database id that is stable across saves, ours is a save-local uid. Nothing here says "
        "our third word is fmsave's 'third word'.",
        "Whether our second/third words map to (database id, save-local id) in either order is "
        "not decided by either side.",
    ),
    X(
        "X03",
        "0xFFFFFFFF as the empty-uid sentinel",
        (
            "scratch/t92/out/schema_v113.json#/table45_structure_e132_e138/three_columns_e132",
            "L1 external anchor / L2 table",
            "u8@4 rec_type 255 = null (38,968 rows); u32@5 person-uid 0xffffffff marks empty; "
            "37 distinct rec_type values, 35,926 distinct person uids.",
        ),
        [
            (
                FMSAVE,
                "src/fmsave/readers/club_table.py:101-103",
                "A row is rejected when its uid is 0 or 0xFFFFFFFF, or repeats an earlier uid.",
                "grammar",
            )
        ],
        "code_agreement",
        "fmsave treats 0xFFFFFFFF as 'no such record'; we read it as 'no such person'. The "
        "agreement is on the sentinel value only -- fmsave's context is a club table, ours is a "
        "person link column.",
        "fmsave also rejects uid 0 while our club table accepts uid 0 (ext/fmsave models/clubs.py"
        ":50 says 0 is a valid club uid) -- an unresolved tension inside fmsave itself.",
    ),
    X(
        "X04",
        "251 rows: table_9 vs the fmsave nation table",
        (
            "scratch/t92/out/schema_v113.json#/table9_closure_e127/profile_members",
            "L2",
            "table_9 is per-nation with exactly 251 rows on both archives, 92 distinct body "
            "lengths, exact closure 13 + sum(body) + 12*rows + 9 = payload.",
        ),
        [
            (
                FMSAVE,
                "src/fmsave/_layouts/fm26_26_3_2.py:1184",
                "NATION_TABLE row_count=251, walked with 14 counted RecordSteps and a "
                "1..2**31-1 database-id range.",
                "grammar",
            )
        ],
        "structural_match",
        "Equal row counts on a per-nation container is suggestive, not probative: fmsave walks a "
        "game_db section with a step script, we walk per-row closures in a client/server table. "
        "Neither reader ever reads the other's bytes.",
        "fmsave's nation table and our table_9 may both be keyed on the 251 nations while holding "
        "different content (national teams vs nation rows).",
    ),
    X(
        "X05",
        "tagged-stream tag vocabulary vs our 34 L3 4CC slot tags",
        (
            "scratch/t88/out3/slots.json",
            "L3",
            "34 mapped codes carry wire tags stdt/endt/comp/gols/ogls/atte/stid/stnm/fsgt/otht/"
            "stdb, each anchored to the RECORD_GET dispatch at exe 0x1543ca0.",
        ),
        [
            (
                FMSAVE,
                "src/fmsave/_layouts/fm26_26_3_2.py:1211-1221,1234-1247",
                "TAGGED_STREAM: 4-byte tags stored byte-reversed, separator 0x01, type codes "
                "u8 0x11 / u16 0x12 / u32 {01,02,03,0B,0F} / string 0x1A / list 0x0A / nil 0x00; "
                "TRANSFER_WINDOWS names tags stdt, endt, dyom, mont, year, wnCT, wnty.",
                "grammar",
            )
        ],
        "naming_match",
        "Two of our ten tags (stdt, endt) also appear in fmsave's transfer-window stream, but our "
        "tags are dispatch cases in the exe while fmsave's are entries in a self-describing list "
        "in a save section. Tag spelling is not a shared record grammar.",
        "If a save-section tag stream ever surfaces in our archives, the fmsave type-code table "
        "would be the first thing to test against it.",
    ),
    X(
        "X06",
        "the null date 0x076C0001, byte-exact across two external repos",
        (
            "scratch/t92/out/schema_v113.json#/stadium_team_l3/stadium_21",
            "L3 (unrelated slot)",
            "Our only date-shaped L3 slots are 2-byte object slots (CHSd/CLAd at reader_off 64) "
            "fed by a u16 reader; we hold no 4-byte wire date grammar.",
        ),
        [
            (
                FMSAVE,
                "src/fmsave/_scan.py:77-87 + src/fmsave/_version.py:65",
                "decode_date reads u16 packed (day-of-year & 0x1FF, flags in the high bits) plus "
                "u16 year 1901..2200; UNSET_GAME_INFO_CLOCK = struct.pack('<HH', 1, 1900).",
                "grammar",
            ),
            (
                FMEDIT,
                "docs/fm24/memory-layout.md:131",
                "A not-listed player's listed date is the packed 1 Jan 1900 value 0x076C0001.",
                "recon",
            ),
        ],
        "code_agreement",
        "pack('<HH', 1, 1900) is exactly 01 00 6c 07 = 0x076C0001, so the two external repos "
        "describe the same 4-byte date encoding in wire and memory respectively. That is external "
        "agreement twice over, and it says nothing about our 2-byte stdt slot.",
        "Our stdt object slot is 2 bytes wide; whether the object converts a 4-byte save date "
        "into that slot is a separate question we have not asked.",
    ),
]


ITEMS += [
    X(
        "X07",
        "stadium capacity and pitch columns",
        (
            "scratch/t92/out/schema_v113.json#/stadium_team_l3/stadium_21/schema_fields",
            "L3 (41 of 60 stadium.xml codes)",
            "server-body offsets: Scpy 0, Sscy 4, Secy 8, Scas 12, Sucy 21, Spln 25 (i16_div10), "
            "Spwd 27, Smnl 54, Smnw 56; client body carries only Scti at 3.",
        ),
        [
            (
                FMEDIT,
                "src/fields/fm24/stadium.rs:22-33 + docs/fm24/memory-layout.md:241-243",
                "Memory: capacity/seated/used/all-seater/expansion at 0x6C/0x70/0x74/0x78/0x7C, "
                "pitch length/width at 0x88/0x8A, 'values are x10: 1050 = 105m'; standing, "
                "environment, condition unmapped.",
                "recon",
            ),
            (
                FMSAVE,
                "src/fmsave/models/stadiums.py:94-112",
                "Wire model: total_capacity, seated_capacity, expansion_capacity, capacity, "
                "pitch_length_dm ... pitch_max_width_dm (decimetres), built/rebuilt dates.",
                "grammar",
            ),
        ],
        "structural_match",
        "All three sides agree a stadium holds five capacity numbers and four pitch numbers in "
        "that conceptual order. But our columns are table_21 server-body offsets, fmsave's are a "
        "save-section struct, and fm-editor's are heap members; the field ORDER differs between "
        "all three, so no offset transfers.",
        "fmsave's dm and fm-editor's x10 both mean tenths of a metre, which makes our i16_div10 "
        "the same unit -- unit agreement only, not slot agreement.",
    ),
    X(
        "X08",
        "club uid and the 'stored value plus one' convention",
        (
            "scratch/t92/out/schema_v113.json#/stadium_team_l3/stadium_21/schema_fields",
            "L3",
            "Stadium duni (index 0) equals rdui (index 1) raw on all 48,413 rows, 0 violations.",
        ),
        [
            (
                FMSAVE,
                "src/fmsave/models/stadiums.py:38",
                "A ground's uid is 'the stored value plus one, the same convention club ...'.",
                "grammar",
            )
        ],
        "naming_match",
        "A +1 convention would break the duni == rdui identity we measured unless both columns "
        "are post-increment. Our measurement stands on its own 48,413 rows; fmsave's note is "
        "about a different container.",
        "Whether table_21 stores uid or uid-1 cannot be settled from fmsave; it needs a stadium "
        "whose game-screen uid we can read.",
    ),
    X(
        "X09",
        "reputation: forwarded club field vs two external sources",
        (
            "scratch/t92/out/schema_v113.json#/stadium_team_l3/club_base18_forwarded_6",
            "L3",
            "Crep forwards CLUB+0x18 index 0 to TEAM+0xa8, wire table_24 TEAM+2..3 as i16; five "
            "more club.xml codes forward the same way (Cdvi/Cldi/Cndi/Codi/Csti).",
        ),
        [
            (
                FMSAVE,
                "src/fmsave/models/clubs.py:69,96",
                "Club.reputation 1..10000, listed in verified=('reputation', "
                "'last_league_position').",
                "grammar",
            ),
            (
                FMEDIT,
                "src/fields/fm24/club.rs:96",
                "c_reputation ships with offset: None (not located) in the FM24 table.",
                "recon",
            ),
        ],
        "range_only",
        "fmsave's 1..10000 range is a claim about save content, and it happens to fit an i16 at "
        "TEAM+2..3. That is a range coincidence; fm-editor, the only source that maps this "
        "entity's memory, could not locate the field at all.",
        "Whether our TEAM+0xa8 i16 and fmsave's Club.reputation are the same number is untested; "
        "a 1..10000 bound would be the first thing to check against a real row.",
    ),
    X(
        "X10",
        "squad status codes, 17 for 17",
        (
            "scratch/t88/out3/slots.json",
            "held (no squad-status slot in our 34 L3 codes)",
            "We hold no squad-status field: none of the 34 mapped 4CC codes is a contract status.",
        ),
        [
            (
                FMSAVE,
                "src/fmsave/models/contracts.py:43-62",
                "SquadStatus: 1 Star Player, 2 Important, 3 Regular Starter, 4 Squad Player, 5 "
                "Impact Sub, 7 Fringe, 9 Emergency Backup, 10 Breakthrough Prospect, 11 Future "
                "Prospect, 13 Youngster, 14 B Team Regular, 15/16/17/18 goalkeepers, 20 Backup, "
                "21 Goalkeeper Emergency Backup, 22 Surplus to Requirements.",
                "grammar",
            ),
            (
                FMLIBRE,
                "docs/recon/fm27-contracts.md:84-100",
                "Same 17 codes on the FM27 heap at contract+0x54, same labels, each with a named "
                "witness player; 6, 8, 12, 18, 19 unseen across 169,023 players.",
                "recon",
            ),
        ],
        "external_agreement_only",
        "Two external repos agreeing on 17 codes is the strongest match in this file and still "
        "changes nothing on our side: neither reads a database table, and we have no slot to "
        "compare against.",
        "fmsave names 18 (Continental Cup Goalkeeper) while FMLibre lists 18 as unseen -- a "
        "disagreement between the two externals, recorded rather than resolved.",
    ),
]


ITEMS += [
    X(
        "X11",
        "rec_type as a family discriminator vs fmsave's counted RecordStep walk",
        (
            "scratch/t92/out/schema_v113.json#/table45_structure_e132_e138/"
            "accessor_view_model_e138",
            "L2",
            "117 club.xml codes are an accessor VIEW: 7 families map to rec_types "
            "{CFG:24, CHA:13, CHS:25, CLA:26, COS:28, CYP:10, CYS:27}, suffix selects row/column.",
        ),
        [
            (
                FMSAVE,
                "src/fmsave/readers/nations.py:28-40",
                "A table is told apart by walking its records whole (RecordStep script), never by "
                "its closing headers, because a record can hold bytes shaped like another header.",
                "grammar",
            )
        ],
        "structural_match",
        "Both sides say a row's byte layout is family-dependent and must be walked with a "
        "per-family script. But fmsave has one script per table, we have seven rec_types in one "
        "table that share one physical row width (rowlen == 80 + namelen for all 84,477 rows).",
        "fmsave's variable-width per-family rows are the opposite finding from our fixed 14-column "
        "row; that contrast is the useful part, and neither side may borrow the other's result.",
    ),
    X(
        "X12",
        "staff job codes",
        (
            "scratch/t92/out/schema_v113.json#/coverage",
            "held",
            "Our coverage no L3 slot for staff job; club/person/team/stadium/comp/nation only.",
        ),
        [
            (
                FMSAVE,
                "src/fmsave/models/staff.py:30-66",
                "StaffJob: 2 Coach, 4 Chairperson, 6 Director, 8 Managing Director, 10 Director of "
                "Football, 12 Physio, 14 Scout, 16 Manager, 20 Assistant, 22 Set Piece, 26 "
                "Fitness, 34 GK Coach, 38 Chief Doctor, 40 Head of Sports Science, ... 88 "
                "Technical Director.",
                "grammar",
            ),
            (
                FMLIBRE,
                "docs/recon/fm27-staff.md:18-23",
                "FM27 heap job codes with counts and witnesses: 38 Chief Doctor 307, 46 Doctor 436, "
                "62 Head Performance Analyst 205, 66 Owner 143.",
                "recon",
            ),
        ],
        "code_agreement",
        "The two externals agree on 38/46/62/66 labels and both disagree about code 8 (fmsave "
        "'Managing Director', FMLibre 'not told apart yet'). We have no slot, so the row stays a "
        "pointer to what an FM26/27 staff table would look like.",
        "FMLibre's code 24 and fmsave's absence of 24 is a gap; neither can be tested here.",
    ),
    X(
        "X13",
        "clause kinds: 14 named by fmsave, 40 tabulated by FMLibre",
        (
            "scratch/t92/out/schema_v113.json#/club_main_row_fields",
            "held",
            "We hold no contract-clause field in any L3 table.",
        ),
        [
            (
                FMSAVE,
                "src/fmsave/models/contracts.py:102-113",
                "ClauseKind: 0x00 min fee release, 0x01 relegation release, 0x02 non promotion, "
                "0x0F top-division relegation salary drop, 0x10/0x11/0x12 foreign/domestic-higher/"
                "domestic release, 0x16 optional extension, 0x20 appearance fee, 0x22 shutout, "
                "0x25 international cap, 0x26 unused sub, 0x29 seasonal landmark G+A.",
                "grammar",
            ),
            (
                FMLIBRE,
                "docs/recon/fm27-contracts.md:11-56",
                "8-byte entries at contract+0x68: u32 amount, u16 condition, u16 kind; 40 kinds "
                "tabulated 0..56 with witnesses.",
                "recon",
            ),
        ],
        "code_agreement",
        "Where they overlap the numbers agree exactly (0 min fee, 1 relegation, 2 non promotion, "
        "15 salary drop, 16/17/18 the release family, 22 extension, 32 appearance, 34 clean "
        "sheet, 37 cap bonus, 38 unused sub, 41 combined G+A). fmsave calls 0x22 SHUTOUT_BONUS "
        "where FMLibre calls 34 Clean Sheet Bonus -- the same concept at a different code, so the "
        "two externally-tagged tables are not interchangeable.",
        "0x22 vs 34 is an open external disagreement about which code is the clean-sheet bonus.",
    ),
    X(
        "X14",
        "nation id vs nation row index",
        (
            "scratch/t92/out/schema_v113.json#/nation_main_row_fields/L3_fields",
            "L3",
            "Five nation slots: Nnsi ref->table 21, Ncti ->5, Nrgi ->19, Ncur ->41, Nndn "
            "u16_bitfield; each carries an object displacement (280/240/248/256/456) and a wire "
            "position.",
        ),
        [
            (
                FMSAVE,
                "src/fmsave/readers/nations.py:1-9",
                "Every nation field elsewhere in a save holds the nation's ROW in the 251-row "
                "table, not its database id; the closing header's second word carries the database "
                "id and is the join to outside lists.",
                "grammar",
            )
        ],
        "structural_match",
        "fmsave's warning -- 'a nation reference is a row index, and only the closing header "
        "carries the database id' -- is the exact distinction our Nnsi/... slots need before any "
        "cross-save join. Our table_9 uid ladder is a row ladder too (5, 6, 7 ... 82082526).",
        "Whether our 5 nation slots hold row indices or database ids is undecided on our side; "
        "fmsave's rule is a hypothesis to test, not a finding we may import.",
    ),
    X(
        "X15",
        "zstd framing of save payloads vs our flat table payloads",
        (
            "scratch/t92/out/schema_v113.json#/table9_closure_e127/closure_claims",
            "L2",
            "Both archives close exactly: client payload 31,956 = 13 + 28,922 + 12*251 + 9; "
            "server payload 307,564 the same shape, one strict tiling solution each.",
        ),
        [
            (
                FMSAVE,
                "src/fmsave/_container.py + _layouts/fm26_26_3_2.py",
                "Save payloads arrive as zstd frames (magic 0xFD2FB528, skippable 0x184D2A50..5F, "
                "128 KiB blocks) and are then split into regions/sections.",
                "grammar",
            )
        ],
        "no_relation",
        "Our client_db/server_db tables are uncompressed payloads with exact closures. fmsave's "
        "container is the layer above any such payload, so its frame grammar cannot confirm our "
        "arithmetic.",
        "If a future archive ever ships compressed, the fmsave frame grammar is the reference.",
    ),
    X(
        "X16",
        "row-count header vs count field bounds",
        (
            "scratch/t92/out/schema_v113.json#/table9_closure_e127/chains",
            "L2",
            "header_record_count 251 equals walked rows on both archives; count is a u32 at "
            "header+9.",
        ),
        [
            (
                FMSAVE,
                "src/fmsave/_layouts/fm26_26_3_2.py:309-310 + readers/club_table.py:87-93",
                "CLUB_TABLE: header_bytes=5, count_range=(1, 200_000); a count outside the range "
                "or larger than len//12 is rejected before the walk.",
                "grammar",
            )
        ],
        "structural_match",
        "Both sides treat a declared count as a claim to be validated against the bytes, not as "
        "truth. Our closure already does this arithmetically; fmsave does it with a range guard.",
        "Our count sits at header+9 while fmsave's is at header+0 with a 5-byte head -- a "
        "different placement for the same idea.",
    ),
]


ITEMS += [
    X(
        "X17",
        "a person uid seen in both a client table and a live process",
        (
            "scratch/t92/out/schema_v113.json#/table45_structure_e132_e138/three_columns_e132",
            "L1 external anchor inside an L2 table",
            "u32@5 is a person uid: C.Ronaldo 735216 appears on 18 rows; 35,926 distinct; "
            "external anchor provenance ext/fm-data@d7a7150.",
        ),
        [
            (
                FMEDIT,
                "docs/fm24/memory-layout.md:70-72",
                "The player object carries its UID at 0x284 in live memory (witnesses found by "
                "searching the heap for that uid).",
                "recon",
            )
        ],
        "id_namespace_only",
        "Both sides name a 'person uid' and both can point at Ronaldo, but 735216 is an FM24 "
        "database id while our anchor is already external to this task. Agreeing the number "
        "exists in two places says nothing about column 5's semantics.",
        "Our col5 is 35,926 distinct over 84,477 rows; if it were the FM24 person id it should be "
        "far denser. That density gap is unexplained and stays unexplained.",
    ),
    X(
        "X18",
        "build gating: fmsave's layout ladder vs fm-editor's fingerprint",
        (
            "scratch/t92/out/schema_v113.json#/incremental_provenance",
            "n/a (our assets are archive tables, not per-build saves)",
            "Our tables are read from a frozen archvie pair with no build gate at all.",
        ),
        [
            (
                FMSAVE,
                "src/fmsave/_version.py + _layouts/__init__.py",
                "A layout is selected by (region, schema, build) with a gating ladder and a "
                "FALLBACK_BUILD; SUPPORTED_GAME_MAJOR = 26 rejects other majors outright.",
                "grammar",
            ),
            (
                FMEDIT,
                "docs/fm24/memory-layout.md + src/fields/fm24/mod.rs",
                "FM24 has no game_plugin.dll -- every entity RVA lives in fm.exe, image base "
                "0x140000000; a separate build fingerprint marks the Epic build.",
                "recon",
            ),
        ],
        "structural_match",
        "Both externals accept that offsets are build-scoped and must be gated, and both refuse "
        "to guess across builds. That is a method agreement, useful as a caution, not as evidence.",
        "Our archive tables carry a schema word (f1 0d) that we do not yet gate on; fmsave's "
        "ladder is the shape such a gate would take.",
    ),
    X(
        "X19",
        "memory-offset tables vs wire-offset tables: the conflation trap",
        (
            "scratch/t92/out/schema_v113.json#/stadium_team_l3/stadium_21/schema_fields",
            "L3",
            "Our stadium slots are WIRE offsets inside a table body (client 3, server 0..56) plus "
            "a separate object displacement (+0x0c etc.).",
        ),
        [
            (
                FMEDIT,
                "src/fields/fm24/stadium.rs:1-25",
                "The same 14 stadium fields are described as live-memory offsets in a 0xB0-stride "
                "object reached through club.home_stadium.",
                "recon",
            )
        ],
        "naming_match",
        "Same field names (UID/name/capacity/seated/expansion/pitch length/pitch width), "
        "completely different coordinate systems. A reader who mixed these up would place our "
        "wire columns at heap offsets.",
        "Only a live-memory capture of the same object could relate the two, and that is outside "
        "this task by construction.",
    ),
    X(
        "X20",
        "what the externals hold that we do not",
        (
            "scratch/t92/out/schema_v113.json#/coverage",
            "held",
            "We hold 34 L3 slots (club 13, comp 49, nation 5, stadium 41, team 11 + forwarded 6) "
            "and 0 L4.",
        ),
        [
            (
                FMSAVE,
                "src/fmsave/models/*",
                "20 record types modelled to field level: Player 53, Staff 31, Contract 25, "
                "Stadium 20, Club 13, Competition 4, Team 4, Nation 2, plus matches/training/"
                "tactics/finances/facilities/affiliates/loans.",
                "grammar",
            ),
            (
                FMLIBRE,
                "docs/recon/ (22 docs)",
                "FM27 recon on bans, debts, loans, transfers, offers, prize money, sponsorships, "
                "youth intake, national teams, tactics and value, object pools, 5 Steam builds.",
                "recon",
            ),
        ],
        "coverage_gap",
        "The externals cover contract clauses, loans, transfer offers, prize money and "
        "sponsorships -- areas where our coverage has no L3 slot at all. They are a reading list, "
        "not a grade.",
        "Every one of these areas would need our own probe before it could carry any grade.",
    ),
]


SUMMARY = {
    "entry_count": len(ITEMS),
    "by_relation": {},
    "held_count": sum(1 for x in ITEMS if x["verdict"] == "held"),
    "grade_moves": 0,
    "note": (
        "Every row is held. No row asserts that an external corpus confirmed, weakened or "
        "re-graded one of our fields; each row records what the two sides say and why the "
        "distance between them is still open."
    ),
}


def build() -> dict:
    from collections import Counter

    by_rel = Counter(x["relation"] for x in ITEMS)
    summary = dict(SUMMARY)
    summary["by_relation"] = dict(sorted(by_rel.items()))
    return {
        "schema": "t93/crosswalk/v1",
        "generated": "2026-11-22",
        "provenance_external": PROV,
        "provenance_internal": INTERNAL,
        "policy": POLICY,
        "summary": summary,
        "entries": ITEMS,
    }


def selftest() -> int:
    assert len(ITEMS) >= 16, len(ITEMS)
    ids = [x["id"] for x in ITEMS]
    assert len(set(ids)) == len(ids), "duplicate id"
    for x in ITEMS:
        assert x["verdict"] == "held", x["id"]
        assert x["relation"] in {
            "structural_match",
            "code_agreement",
            "naming_match",
            "id_namespace_only",
            "range_only",
            "external_agreement_only",
            "coverage_gap",
            "no_relation",
        }, x["id"]
        assert x["why_not_upgraded"].strip(), x["id"]
        assert x["residual"].strip(), x["id"]
        assert x["external_side"], x["id"]
        for e in x["external_side"]:
            assert e["provenance"].split("@")[0] in PROV, (x["id"], e["provenance"])
            assert "@" in e["provenance"], x["id"]
            assert e["locator"].strip() and e["statement"].strip()
        o = x["our_side"]
        # our grade must be one we already own, never an external label
        assert o["grade"].startswith(("L1", "L2", "L3", "held", "n/a")), (x["id"], o["grade"])
        assert not o["grade"].lower().startswith("ext"), x["id"]
        assert "verified" not in o["grade"].lower(), x["id"]
        assert "unconfirmed" not in o["grade"].lower(), x["id"]
    totals = build()["summary"]
    assert totals["held_count"] == len(ITEMS) and totals["grade_moves"] == 0
    print(f"selftest OK: {len(ITEMS)} entries, all held, 0 grade moves")
    return 0


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    if "--out" in argv:
        dest = argv[argv.index("--out") + 1]
        payload = build()
        with open(dest, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        print(f"wrote {dest} {payload['summary']['entry_count']} entries")
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
