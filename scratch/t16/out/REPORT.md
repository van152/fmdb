# t16 serializer walk — partial

Status: `partial_golden_gate_failed`. t14 stage2_map.json passed precondition with status `complete`.

## Method implemented

- Per-class factory handler comes from the frozen t14 census; direct call targets are walked with a visited set to depth 4. Targets called by more than 50 factory handlers are skipped as shared runtime.
- Class RTTI vtable slot 19 is read from the verified class vtable; bounded direct-call BFS follows thunks/wrappers and scans `mov r8d, imm` + stream virtual calls, propagating simple record-base LEA/MOV aliases.
- Exact code matches require a unique `(object_off, width, 4CC)` direct-read instance compatible with the schema type. Ambiguities are kept in conflicts; fields without evidence remain unnamed.
- Engine outputs are candidates only where fixed linear path assumptions are not closed; gold baselines are labeled inherited, never silently attributed to t16.

## Golden gate

### city: `fail`

- baseline_status: `pass`
- named_reference_fields: `['Clgi', 'Clri', 'Cnti', 'Cwea']`
- engine_named_reference_fields: `[]`
- engine_fields_named: `1`
- engine_conflicts: `[]`
- row_count: `56293`

### weather: `fail`

- expected_l3_fields: `89`
- schema_target_fields_found: `89`
- available_baseline_artifacts: `[]`
- failure: `E27 89-field offset artifact is absent from this workspace; seasonal 4CCs are not enough to infer row offsets.`

### comp: `fail`

- baseline_status: `pass`
- engine_fields_named: `0`
- engine_reproduced_fields: `0`
- engine_matched_codes: `[]`
- engine_conflicts: `[{'field': 'duni', 'reason': 'duplicate_schema_code', 'candidate_count': 0, 'candidates': []}, {'field': 'duni', 'reason': 'duplicate_schema_code', 'candidate_count': 0, 'candidates': []}, {'field': 'RsL0', 'reason': 'duplicate_schema_code', 'candidate_count': 0, 'candidates': []}, {'field': 'RsL0', 'reason': 'duplicate_schema_code', 'candidate_count': 0, 'candidates': []}, {'field': 'COPc', 'reason': 'duplicate_schema_code', 'candidate_count': 0, 'candidates': []}, {'field': 'COPc', 'reason': 'duplicate_schema_code', 'candidate_count': 0, 'candidates': []}, {'field': 'CTty', 'reason': 'fresh_walk_conflicts_with_frozen_golden', 'expected': {'offset': 18, 'width': 1}, 'observed': {'offset': 6, 'width': 1, 'inst_off': '0xeb711a'}}]`
- expected_fields: `18`
- rechecked_fields: `18`
- matched_fields: `18`

## Scope and unresolved

Weather E27's 89 L3 expected offsets are not present in this workspace. t12 has sparse weather path-descend records, not the 88 seasonal offsets; these offsets were not synthesized. Because weather fails the gate, no 10-entity batch was released.

City and comp field tables contain explicitly marked inherited E55/E20 baselines; they do not assert fresh full engine reproduction. `fields_nati.json` retains seven t01g L3 prefix fields as inherited evidence; fresh nation walk named none. `fields_weather.json` preserves every schema field as unnamed.

Factory/reader traces for a single debug entity are produced by `--entity <name>`. Existing scratch/t05..t14, reports, docs, and evidence were read-only; writes stayed in `scratch/t16/out/` and the new `scripts/t16_serializer_walk.py`. No game/editor/IDA was launched.

## Single-entity debug walks

### city: walked 1 class branches; 1 / 15 top-level fields named by fresh walk.

- table 2 `CITY`: ok; slot19=0xe54c20; vtable assignment=True; candidate serializer branches: 0x3aa5550:10 events.

### club: walked 15 class branches; 0 / 433 top-level fields named by fresh walk.

- table 3 `LEAGUE_BODY_CLUB`: ok; slot19=0x157cff0; vtable assignment=True; candidate serializer branches: 0xe5a7a0:6 events, 0x43beba0:2 events.
- table 33 `STARTING_CLUB_DEBT`: ok; slot19=0x15350f0; vtable assignment=False; candidate serializer branches: 0x4367ac0:18 events.
- table 34 `STARTING_TEAM_CUP_HISTORY`: ok; slot19=0x156efd0; vtable assignment=True; candidate serializer branches: 0x43a6890:11 events.
- table 37 `STARTING_TEAM_LEAGUE_HISTORY`: ok; slot19=0x119ddf0; vtable assignment=True; candidate serializer branches: 0x3e62b90:14 events.
- table 43 `STARTING_MONTHLY_INSTALLMENT`: ok; slot19=0x153c6a0; vtable assignment=True; candidate serializer branches: 0x4370860:6 events.
- table 50 `STARTING_MLS_TRADED_SLOT`: ok; slot19=0x1584400; vtable assignment=True; candidate serializer branches: 0x43d7b10:4 events.
- table 51 `STARTING_MLS_GENERAL_ALLOCATION_MONEY`: ok; slot19=0x152f0b0; vtable assignment=False; candidate serializer branches: 0x4357bf0:3 events.
- table 58 `STARTING_WEEKLY_WAGE_CONTRIBUTION`: ok; slot19=0x153d2b0; vtable assignment=True; candidate serializer branches: 0x43722a0:5 events.
- table 60 `STARTING_MLS_TARGETED_ALLOCATION_MONEY`: ok; slot19=0x152f0b0; vtable assignment=True; candidate serializer branches: 0x4357bf0:3 events.
- table 61 `STARTING_ITALIAN_SERIE_A_CLUB_THAT_FREED_UP_NON_EU_SLOT`: ok; slot19=0x1584620; vtable assignment=True; candidate serializer branches: 0x43d81b0:3 events.
- table 62 `STARTING_RESERVE_TEAM`: ok; slot19=0x119bf60; vtable assignment=True; candidate serializer branches: 0x3e5d730:11 events.
- table 63 `STARTING_ITALIAN_SERIE_A_CLUB_NON_EU_SLOTS_NUMBER`: ok; slot19=0x1584620; vtable assignment=True; candidate serializer branches: 0x43d81b0:3 events.
- table 64 `STARTING_CLUB_STAFF_JOB_STATUS`: ok; slot19=0x1583950; vtable assignment=True; candidate serializer branches: 0x43d4a10:4 events.
- table 66 `STARTING_CLUB_TRANSFER_PREFERENCE`: ok; slot19=0x152f720; vtable assignment=True; candidate serializer branches: 0x43583b0:5 events.
- table 70 `STARTING_VISION_OBJECTIVE`: ok; slot19=0x1454a10; vtable assignment=True; candidate serializer branches: 0x4214ce0:12 events.

### comp: walked 2 class branches; 0 / 255 top-level fields named by fresh walk.

- table 25 `COMP`: ok; slot19=0xed0a40; vtable assignment=True; candidate serializer branches: 0xeb7000:9 events.
- table 26 `COMP_HISTORY_RECORD`: ok; slot19=0x1567ab0; vtable assignment=True; candidate serializer branches: 0x4396c20:1 events.

### nation: walked 1 class branches; 0 / 346 top-level fields named by fresh walk.

- table 10 `NATION`: ok; slot19=0x103fac0; vtable assignment=True; candidate serializer branches: 0x103fac0:2 events.

