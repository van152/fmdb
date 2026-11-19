# t54 v6 Merge Report

Status: schema v6 generated additively from the SHA-pinned v5/fix1 pair; t53 E93 is accepted at L2.

## Result

- TCrs main vector: `table_9.dat` / `this+0x188`; getter vector: typed suffix of `table_extra_9.dat` / `[this+0xb0]+0x48`.
- Main server closure: 166/85 presence and 2,219 items; getter suffix: 179/72 presence, 39 zero-count vectors, 76 items. Both members close at EOF in both archives.
- PUnI/PUnT/PUnP/PUnJ remain held; no L3 field mapping is attributed to E93.
- The six v5 slot19 rejection records remain intact. Eight t53 negative trial groups are itemized; nation negative records are 15, held count remains 20.
- The t50 `NO WINNER` t9 framing decision remains intact. t53 only resolves the table_extra_9 internal block candidates and appends that result.
- EDfx scope is editor-only generated output on the traced route; upstream input persistence is outside scope. EDsc remains without a verified call chain.
- Protected v5 tables, regressions, v3 baseline, club auxiliary source, club coverage, and nation_static_side are unchanged.
- L4=0; no game/editor/IDA, network, or Z: access.

## Outputs

- `reports/club_nation_subtable_schema.json` and `.md`: v6 pair.
- `scratch/t54/out/club_nation_subtable_schema.v5.json` and `.md`: SHA-pinned v5 input snapshots.
- `scratch/t54/out/ledger_snapshot.json`: exact ledger bytes used for E93 provenance.
- `scratch/t54/out/consolidate_v6.py`: deterministic guarded builder with `--help` / `--selftest` / `--build`.
- `scratch/t54/out/verify.py`: independent verifier; it does not import the builder.
- `scripts/t54_spot_v6.py`: independent spot script; it does not import the builder.
- `scratch/t54/out/spot_*.log`: command outputs and anchor regression.

Coverage check: 30 L3 / 30 unique / 20 held / 15 negative; t53 groups=8.

## Audit

v5 JSON SHA-256 `03967c9157fe0ca46d741e5bd74f9cd4d8df592045ca2dd6c38827f99eb36184`; v5 Markdown SHA-256 `4e40595cb7734df534c4ab145b96855fada9da38f711454f27d3cfedf5e6c009`. E93 claim SHA-256 `a889360cc8ac6a2eca46190000b28d8dcadee8a79705c2f30283f90b1542e30c`. Verification commands and results are in `spot_*.log`.
