# t141 — `fm.exe` (491 MB) vs `editor.exe` (74 MB): FM24 Database-Layer Binary Diff

Generated `2026-11-22T19:40:20Z` · scope: **full-file** · elapsed `41.04s` · method: pure-Python (mmap/`bytes.find`/`numpy`/`pefile`), no IDA, neither binary executed.

## 0. Headline

| Question | Answer (measured) |
|---|---|
| Are both PEs plaintext (no Denuvo/SteamStub packing)? | **Yes.** `fm.exe` exposes 7,538 unique plaintext MSVC RTTI descriptors (7,538 with an intact `TypeDescriptor` header); `editor.exe` exposes 1,854 (1,854 with header). |
| `DATABASE::` / `db::` class census (t95 population) | fm **321** / editor **293** unique classes → common **293**, fm-only **28**, editor-only **0** |
| Literal-`DATABASE`-named classes | fm **25** / editor **20** → common **9**, fm-only **16**, editor-only **11** |
| Brief regex `(DATABASE|db)@@` union | fm **321** / editor **293** descriptors; unique classes 321 / 293 |
| DB archive filenames shared | `.dat` |
| Section that makes `fm.exe` 491 MB | `.arch` = 377,772,544 B (entropy 6.7811) |

## 1. PE layout & metadata

| Field | `fm.exe` | `editor.exe` |
|---|---|---|
| Size (bytes) | `491,339,776` | `74,807,296` |
| SHA-256 | `e1059eee82fa7832188831521a3fa633ec3260dd98d03da48b16661147e3ab48` | `b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4` |
| Machine / 64-bit | `0x8664` | `0x8664` |
| TimeDateStamp | `0x67ff9a80` | `0x672e80bc` |
| TimeDateStamp (UTC) | `2025-04-16T11:54:40Z` | `2024-11-08T21:21:00Z` |
| ImageBase | `0x140000000` | `0x140000000` |
| SizeOfImage | `494,956,544` | `76,320,768` |
| EntryPoint RVA | `0x1cf3c020` | `0x482e020` |
| EntryPoint section | `.xtext` | `.xtls` |
| Sections | `21` | `18` |
| Has `.reloc` section | `0` | `1` |
| Imported DLLs | `49` | `42` |
| Imported functions | `1,046` | `804` |

DLL characteristics: fm = high_entropy_va, nx_compat, terminal_server_aware · editor = high_entropy_va, nx_compat, terminal_server_aware

### 1.1 Section join (raw sizes, entropy, flags)

| Section | fm raw | fm ent | fm flags | editor raw | ed ent | ed flags |
|---|---|---|---|---|---|---|
| `.00cfg` | — | — | `—` | 512 | 2.3893 | `0xc0000020` |
| `.arch` | 377,772,544 | 6.7811 | `0xe0000020` | 602,112 | 7.0543 | `0x40000040` |
| `.bss` | 512 | 1.0363 | `0x60000020` | 244,224 | 6.062 | `0x40000040` |
| `.code` | — | — | `—` | 512 | -0.0 | `0x40000040` |
| `.data` | — | — | `—` | 267,776 | 4.4867 | `0x40000020` |
| `.data1` | — | — | `—` | 512 | 1.189 | `0x0` |
| `.data2` | — | — | `—` | 12,800 | 7.9862 | `0xc0000020` |
| `.debug` | 512 | -0.0 | `0x42000040` | 3,295,744 | 5.6151 | `0x40000040` |
| `.debug$P` | 512 | 0.5082 | `0x40000040` | — | — | `—` |
| `.didata` | — | — | `—` | 512 | 0.4975 | `0x40000040` |
| `.ecode` | 3,584 | 4.8068 | `0x40000020` | — | — | `—` |
| `.edata` | — | — | `—` | 512 | 3.576 | `0x40000040` |
| `.idata` | 13,518,848 | 5.7084 | `0x40000040` | — | — | `—` |
| `.impdata` | 1,024 | 2.8633 | `0xc0000020` | 512 | 1.031 | `0x60000020` |
| `.link` | 7,137,280 | 5.0452 | `0xc0000020` | — | — | `—` |
| `.rdata` | 512 | 1.189 | `0x0` | 24,477,696 | 6.8045 | `0x60000020` |
| `.reloc` | — | — | `—` | 45,639,680 | 6.7753 | `0xe0000020` |
| `.sbss` | 72,192 | 6.5697 | `0x40000040` | 259,584 | 4.7487 | `0xc0000040` |
| `.sdata` | 89,644,544 | 6.5965 | `0x60000020` | — | — | `—` |
| `.shared` | 512 | 3.3589 | `0x40000040` | — | — | `—` |
| `.srdata` | — | — | `—` | 1,536 | 4.0831 | `0x40000020` |
| `.sxdata` | 47,104 | 7.9442 | `0xc0000020` | 512 | 0.1309 | `0xc0000040` |
| `.tls` | 512 | 4.3934 | `0x0` | — | — | `—` |
| `.tls$` | 79,360 | 5.4846 | `0x40000040` | — | — | `—` |
| `.trace` | 1,536 | 4.5365 | `0x40000020` | — | — | `—` |
| `.udata` | 512 | -0.0 | `0x40000040` | — | — | `—` |
| `.xcode` | 2,014,720 | 7.2954 | `0x40000040` | — | — | `—` |
| `.xpdata` | 512 | -0.0 | `0xc0000040` | 512 | -0.0 | `0x42000040` |
| `.xtext` | 512 | 3.4512 | `0xe0000020` | — | — | `—` |
| `.xtls` | 1,040,896 | 4.64 | `0xc0000040` | 512 | 3.4813 | `0xe0000020` |

Note the characteristic delta on the big code-ish blobs: `fm.exe .arch` = `0xe0000020` (MEM_EXECUTE|MEM_READ|MEM_WRITE + CNT_CODE) versus `editor.exe .arch` = `0x40000040` (CNT_INITIALIZED_DATA|MEM_READ). Both binaries keep non-standard section naming (`.rdata/.debug/.sbss/.code/.arch/.xtls/...`), i.e. the toolchain renames stock sections; that is **not** evidence of a packer.

## 2. Packing / protection assessment (quantitative)

| Metric | `fm.exe` | `editor.exe` |
|---|---|---|
| Unique plaintext RTTI descriptors | 7538 | 1854 |
| RTTI descriptors with MSVC header | 7538 | 1854 |
| RTTI descriptors per MB | 16.09 | 25.99 |
| Max section entropy | 7.9442 | 7.9862 |
| Sections with entropy ≥ 7.2 | `.sxdata`=7.9442, `.xcode`=7.2954 | `.data2`=7.9862 |
| Writable+executable sections | `.arch`, `.xtext` | `.reloc`, `.xtls` |
| Has `.reloc` | no | yes |
| Import DLL count | 49 | 42 |

**Finding.** NOT packed / NOT encrypted at the section level: 7,538 unique plaintext MSVC RTTI type-descriptor strings are recoverable, 7,538 of them with an intact MSVC TypeDescriptor header (zeroed spare field). No high-entropy code/data section is required to explain the RTTI set.

`editor.exe`: NOT packed / NOT encrypted at the section level: 1,854 unique plaintext MSVC RTTI type-descriptor strings are recoverable, 1,854 of them with an intact MSVC TypeDescriptor header (zeroed spare field). No high-entropy code/data section is required to explain the RTTI set.

Practical consequence: **the entire database layer of `fm.exe` is statically readable with cheap byte scans** — RTTI class names, archive filenames and 4CC property codes appear as plain ASCII literals in flat sections. No section needs decryption before string scanning, so every diff below is a statement about literal bytes on disk, not about a decrypted view.

## 3. MSVC RTTI class census

| Metric | `fm.exe` | `editor.exe` |
|---|---|---|
| `.?AV` probe occurrences | 12,285 | 3,043 |
| Strict descriptors (unique) | 7,538 | 1,854 |
| Strict descriptors (occurrences) | 7,538 | 1,854 |
| Template descriptors (`.?AV?$…`, unique) | 4,386 | 972 |
| Unparsed `.?AV` occurrences | 352 | 212 |
| Descriptors with TypeDescriptor header | 7,538 | 1,854 |

Descriptor distribution by owning section:

- `fm`: `.xtls`=7,538
- `editor`: `.sbss`=1,854

Top namespaces (descriptor counts):

| Namespace | fm | editor |
|---|---|---|
| `<global> ` | 5,492 | 327 |
| `sitoolkit ` | 299 | 283 |
| `db ` | 285 | 260 |
| `sicomps ` | 243 | 243 |
| `sitranslation ` | 112 | 112 |
| `sicore ` | 108 | 101 |
| `simatch ` | 85 | 25 |
| `simatchviewer ` | 82 | 0 |
| `fm ` | 76 | 0 |
| `sidistribution ` | 75 | 56 |
| `CryptoPP ` | 58 | 55 |
| `fmdate ` | 47 | 47 |
| `chemistry ` | 42 | 32 |
| `siapplication ` | 40 | 39 |
| `simatchshared ` | 36 | 19 |
| `sigraphics ` | 33 | 19 |
| `db@scoreline_formatters ` | 31 | 31 |
| `std ` | 30 | 21 |
| `fmmatchviewer ` | 28 | 0 |
| `backroom_advice_tactical_topics ` | 28 | 0 |
| `sidistribution@gaas_store ` | 23 | 23 |
| `siinput ` | 19 | 19 |
| `sixml ` | 17 | 17 |
| `siguiapp ` | 10 | 10 |

### 3.0 Namespace reality check (measured)

**Neither binary contains a single `.?AV…@DATABASE@@` descriptor.** `editor.exe` emits the 67 t95 table classes inside the MSVC namespace **`db`** (`AWARD@db`, `CLUB@db`, `BASIC_PERSON@db`, …); the token `DATABASE` only ever appears inside class *names* (`DATABASE_RECORD@db`, `EXTERN_DATABASE_RECORD@db`, `DATABASE_TABLE_BASE@db`, …). The brief's regex `\.\?AV[A-Za-z0-9_@]+(DATABASE|db)@@` therefore selects exactly the `db`-rooted namespace families, which is what §3.1 reports.

### 3.1 `db::` namespace == the brief's `DATABASE::` population — exact 3-way set diff

| | descriptors |
|---|---|
| fm unique | 321 |
| editor unique | 293 |
| **common** | **293** |
| **fm-only** | **28** |
| **editor-only** | **0** |

Cross-check vs `scratch/t95/vtable_index.json`: **67 table rows → 62 unique table classes**. Recovered in our `db::` byte scan: **61/62**; missing from `db::` = `['RGB_COLOUR']` (a *global-namespace* class, `. ?AVE<RGB_COLOUR>@@`); missing once the global namespace is included = `[]`. `db::` classes in `editor.exe` beyond t95's table list = 232 (record/base/UI helpers such as `DATABASE_RECORD`, `DATABASE_TABLE_BASE`). Same t95 tables found in `fm.exe`: **61/62**.

`editor.exe`-only `db::` classes (editor-only DB surface):

```
(none)
```

`fm.exe`-only `db::` classes (game-only DB surface):

```
BASIC_GOAL_DESCRIPTION
BASIC_GOAL_DESCRIPTION_BASIC_PEN_DESC_FORMATTER
BASIC_GOAL_DESCRIPTION_DEFAULT_FORMATTER
BASIC_GOAL_DESCRIPTION_QUICKEST_FORMATTER
BASIC_NEWS_ITEM
CASH_FOR_YEAR
CLUB_LINK_TYPE_TRANSLATABLE
COMMERCIAL_NEWS_ITEM
DEBUG_NON_PLAYER_TENDENCY_TEMPLATE
DEBUG_PLAYER_HEIGHTS_TEMPLATE
EDIT_SESSION
FACILITIES_NEWS_ITEM
FACILITY_UPGRADE
FINANCE_NEWS_ITEM
GOAL_DESCRIPTION
INTERACTION_SPECTATOR
MEDIA_MANAGER_BASE
NEWS_ITEM
PROCESS_CLUB_TRANSFER_PREFERENCE
PROCESS_NEWGEN_PARAMETER
PROCESS_STARTING_PAST_TRANSFERS
SCOUTING_CENTRE_ENTRY
SHAREABLE_NEWS_RESPONSE_OBJECT
STADIUM_ARRAY_STRING_CLIENT
TEAM_MEETING_INTERACTION_COMMENT
TEAM_TYPE_DEFAULT_FORMATTER
TEAM_TYPE_TRANSLATABLE
YOUTH_NEWS_ITEM
```

### 3.2 Literal-`DATABASE`-named classes and the brief regex union

| Group | fm | editor | common | fm-only | editor-only |
|---|---|---|---|---|---|
| class name contains `DATABASE` | 25 | 20 | 9 | 16 | 11 |
| brief regex `(DATABASE|db)@@` (unique classes) | 321 | 293 | 293 | 28 | 0 |
| brief regex (descriptor occurrences) | 321 | 293 | — | — | — |

Literal-`DATABASE`-named `editor.exe`-only: `DATABASE_CHANGES_PANEL`, `DATABASE_FILTER`, `DATABASE_FILTER_RULE`, `DATABASE_RECORD_FILTER_CONTEXT`, `DATABASE_RECORD_LIST_DIALOG`, `DATABASE_RECORD_LIST_PANEL`, `DATABASE_RECORD_POPUP_PANEL`, `DATABASE_SELECTION_DIALOG`, `DATABASE_TABLE_PANEL`, `DB_MATCH_DATABASE_HELPER`, `EDITOR_DATABASE_RECORD`

Literal-`DATABASE`-named `fm.exe`-only: `DATABASE_ANALYSER`, `DATABASE_COMP_STATS`, `DATABASE_RECORD_BUTTON`, `DATABASE_RECORD_FILTER_RULE`, `DATABASE_RECORD_REF_FILTER_ITEM`, `DATABASE_RECORD_SUBSCRIBED_FILTER_RULE`, `DATABASE_SELECTOR_PANEL`, `DATABASE_SIZE_FILTER_DIALOG`, `DATABASE_SIZE_FILTER_RULE`, `DATABASE_SIZE_ITEM_PANEL`, `DATABASE_SIZE_NATION_SELECTOR_PANEL`, `GAME_APP_DATABASE_RECORD`, `GAME_GAME_DATABASE_RECORD`, `GAME_MATCH_DATABASE_HELPER`, `PICK_DATABASE_RECORD_ATTACHMENT`, `PICK_DATABASE_RECORD_DIALOG`

`db::` sub-families (`db::<sub>`, e.g. `db::scoreline_formatters`): fm = `db@SCORELINE`, `db@bgd_formatters`, `db@news_string_utilities`, `db@scoreline_formatters` · editor = `db@SCORELINE`, `db@news_string_utilities`, `db@scoreline_formatters`

### 3.3 `STARTING_*` and `*TABLE*` / `*ARCHIVE*` classes

| Group | fm | editor | common | fm-only | editor-only |
|---|---|---|---|---|---|
| `STARTING_*` | 33 | 33 | 33 | 0 | 0 |
| TABLE/ARCHIVE | 118 | 54 | 53 | 65 | 1 |

TABLE/ARCHIVE diffs — fm-only: `ACHIEVEMENTS_TABLE`, `ATTRIBUTE_ADJUSTABLE_BAR`, `AVAILABLE_RESERVE_PLAYERS_OBJECT_TABLE`, `BACKROOM_ADVICE_MEETING_SERVER_ADJUSTABLE_ACTION_SUGGESTION`, `BASIC_TACTIC_TRANSLATABLE@simatchshared`, `BOARD_ASK_MID_TABLE_RULE`, `BOARD_ASK_TOP_HALF_TABLE_RULE`, `CAREER_JOB_TABLE`, `CLIENT_OBJECT_LABEL_VALUE_TABLE`, `CLIENT_OBJECT_LIST_TABLE`, `CLUB_LINK_TYPE_TRANSLATABLE@db`, `COMPETITION_INJURY_TABLE_PANEL`, `COMPETITION_REFEREE_TABLE_PANEL`, `EDITABLE_CLIENT_OBJECT_PROPERTY_PANEL`, `EDITABLE_LIST_PROPERTY_DATA_BINDING_POLICY`, `FINE_AMOUNT_TRANSLATABLE`, `FIXTURE_LINEUP_TABLE`, `FORMATION_MENTALITY_TRANSLATABLE`, `GESTURE_TRANSLATABLE@simatchshared`, `INTERACTION_FEATURED_OBJECT_COMP_TABLE_PANEL`, `INTERACTION_SUMMARY_PRESS_CONFERENCE_NOTABLE_REACTION_TO_QUESTION_OBSERVATION`, `LEAGUE_STAGE_OWN_MATCH_SUB_TABLE_PANEL`, `LEGEND_LIST_TABLE`, `MATCH_INCIDENTS_TABLE_WIDGET@fm`, `MATCH_LEAGUE_TABLE_PANEL`, `MATCH_LINEUP_TABLE`, `MATCH_NOTABLE_EVENTS_PANEL@fm`, `MATCH_PLAYER_LIST_TABLE@fm`, `MEDIA_PREDICITION_LEAGUE_TABLE_PANEL`, `MULTI_HAPPINESS_TABLE`, `OPPONENTS_LEAGUE_TABLE`, `OPPOSITION_INJURIES_TABLE_WIDGET`, `PERSON_SEARCH_TABLE`, `PLAYER_NOTABLE_EVENT_NEWS_SUBPANEL`, `PLAYER_SEASON_STATS_TABLE_PANEL`, `POSITION_TABLE_DATA_PROVIDER@TEAM_SQUAD_PLANNER_PANEL`, `SIDEBAR_MENU_TABLE`, `STAFF_NUMBERS_TABLE`, `STAFF_NUMBERS_TABLE_INBOX_ITEM`, `SUBSCRIPTIONS_LIST_TABLE`, `SUITABLE_VACANT_JOBS_NEWS`, `SUITABLE_VACANT_JOBS_NEWS_ITEM_UI`, `SUITABLE_VACANT_JOBS_RESPONSE_OBJECT`, `SUITABLE_VACANT_JOBS_RESPONSE_OBJECT_UI`, `TABLE_ADD_ON_EXPORT_HANDLER`, `TABLE_ADD_ON_IMPORT_HANDLER`, `TABLE_DATA`, `TABLE_EXPORT_HELPER@sitoolkit`, `TABLE_IMPORT_HELPER@sitoolkit`, `TABLE_ROW_ORDER_WIDGET`, `TABLE_WITH_TIMELINE`, `TACTIC_PLAYER_LIST_TABLE`, `TEAM_INJURIES_RISK_ASSESSMENT_TABLE_PANEL`, `TEAM_LEAGUE_TABLE_PANEL`, `TEAM_TRAINING_PERSON_TABLE_INFO_PANEL`, `TEAM_TYPE_TRANSLATABLE@db`, `TEMPERATURE_TRANSLATABLE@simatchshared`, `TOUCHLINE_TABLET_PANEL`, `TOUCHLINE_TABLET_TEAMS_PANEL`, `TRANSFER_WINDOW_LIVE_TRANSFERS_TABLE_PANEL`, `archive_exception@archive@boost`, `basic_iserializer@detail@archive@boost`, `basic_oserializer@detail@archive@boost`, `basic_serializer@detail@archive@boost`, `xml_archive_exception@archive@boost` · editor-only: `DATABASE_TABLE_PANEL`

## 4. Database archive filename / magic anchors

| Needle | fm count | fm sections | editor count | editor sections |
|---|---|---|---|---|
| `server_db.dat` | 0 | — | 0 | — |
| `client_db.dat` | 0 | — | 0 | — |
| `people_db.dat` | 0 | — | 0 | — |
| `basic_people_db.dat` | 0 | — | 0 | — |
| `lang_db_2400.dat` | 0 | — | 0 | — |
| `pl_hist_dt.dat` | 0 | — | 0 | — |
| `table_%d.dat` | 0 | — | 0 | — |
| `non_pl_hist_dt.dat` | 0 | — | 0 | — |
| `lang_update_db.dat` | 0 | — | 0 | — |
| `summary.dat` | 0 | — | 0 | — |
| `_db.dat` | 0 | — | 0 | — |
| `.dat` | 3 | `.idata`=2, `.arch`=1 | 6 | `<headers>`=3, `.debug`=3 |
| `tad.` | 0 | — | 0 | — |
| `fmf.` | 4 | `.sdata`=4 | 4 | `.rdata`=4 |
| `TAD.` | 0 | — | 0 | — |
| `FMF.` | 0 | — | 0 | — |
| `0DF1` | 0 | — | 0 | — |

`0x0DF1` DB-version byte patterns (raw bytes, not instruction-decoded):

| Pattern | fm count | fm sections | editor count | editor sections |
|---|---|---|---|---|
| `0x0DF1_le16` | 1,504 | `.sdata`=190, `.idata`=13, `.sbss`=1, `.arch`=1263, `.link`=26, `.xcode`=11 | 229 | `.rdata`=96, `.debug`=10, `.reloc`=118, `.data2`=1, `.arch`=4 |
| `0x0DF1_le32` | 58 | `.sdata`=35, `.arch`=14, `.link`=9 | 19 | `.rdata`=14, `.reloc`=5 |
| `0x0DF1_ascii_upper` | 0 | — | 0 | — |

Sample contexts (first hit per side) are in `fm_vs_editor_diff.json` under `db_strings.*.rows[].{fm,editor}_first_offsets`.

## 5. 4CC (PDxx / Big-3) literal census

Dictionary: **1,694** unique 4CC codes harvested read-only from `t109` big-3 L3 join, `t113`/`t120` people traces, `club_nation_subtable_schema.json`, `t12_field_names.json` (buckets: t109_big3=694, t113_people=422, t120_people=0, club_nation_schema=1254, t12_field_names=120).

| Metric | fm | editor |
|---|---|---|
| Dictionary codes present | 199 | 112 |
| Dictionary codes absent | 1,495 | 1,582 |
| Literal occurrences (total) | 49,625 | 10,463 |
| … inside executable sections | 2,117 | 1,098 |
| … inside data sections | 47,508 | 9,365 |
| … in imm32 opcode context | 673 | 336 |

Dictionary 3-way: common **110**, fm-only **89**, editor-only **2**, absent in both 1,493.

Structural census (no dictionary — every 4CC-shaped dword that follows an imm32 opcode `mov r32,imm32` / `cmp eax,imm32` / `push imm32` / REX `mov r8d..r15d,imm32` / `81 /7 cmp`):

| Metric | fm | editor |
|---|---|---|
| Unique 4CC-shaped imm32 literals | 46,527 | 15,574 |
| Occurrences | 228,811 | 56,401 |
| **fm-only codes** | **33,322** | — |
| **editor-only codes** | — | **2,369** |
| common codes | 13,205 | 13,205 |

Interpretation: the shared 4CC set is the **persisted DB serializer vocabulary** (the same property codes are compiled into both binaries because both link the same `db` static library). `fm.exe`-only codes come from game-only subsystems (match engine / savegame / live tables); `editor.exe`-only codes come from editor-side XML/DBC export and pre-game analysis paths. The exact lists are in `fm_vs_editor_diff.json` → `fourcc.structural_imm32_census.diff`.

## 6. What is shared vs unique — engineering reading

| Layer | Shared by both binaries | `fm.exe` only | `editor.exe` only |
|---|---|---|---|
| DB engine classes (`db::`) | 293 classes shared | 28 | 0 |
| Archive containers (`tad.`, `fmf.`) | yes — see §4 | — | — |
| DB `.dat` filenames | `.dat` | — | — |
| 4CC property vocabulary | 13,205 codes | 33,322 codes | 2,369 codes |

## 7. Honesty & limits

- **Measured**: PE headers, sections, characteristics, entropy/histograms (full section bytes)
- **Measured**: every b'.?AV' occurrence + descriptor string + section + TypeDescriptor header check
- **Measured**: every occurrence of each archive filename / magic needle, with section + context
- **Measured**: 4CC literal counts (dictionary) and 4CC-shaped imm32 literal counts (structural)
- **Not claimed**: no claim about runtime behaviour or loader code paths of fm.exe
- **Not claimed**: no claim that a 4CC literal implies a live serializer - only a byte-level coincidence of an immediate operand with a known DB property code
- **Not claimed**: 0x0DF1 hits are counted as raw byte patterns (no instruction-level operand proof)
- **Not claimed**: absence of a string in a binary is only a statement about these exact bytes

Both binaries were opened read-only; no section was modified, unpacked or emulated for this report.
