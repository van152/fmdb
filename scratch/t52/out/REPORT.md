# t52 v5 Merge Report

Status: complete, with t50/t49 framing conflict recorded and left unresolved.

## Result

- Public schema advanced from v4 to v5 by additive nation sections.
- Protected v4 sections (`tables`, `negative_regressions`, `v3_baseline`, `club_auxiliary_sources`, `nation_data_side_status`) remain structurally identical to the frozen v4 snapshot.
- Nation totals: L3 occurrences=30, unique wire fields=30, held=20, bounded negative records=7.
- t47 Ntxr: 7 L3, 2 held; 1,899 server items, tag 2, 25 bytes each; client mode 0 has no items.
- t49 table_9: 17 L3, 13 held. table_extra_9 remains unbound; 6 rejected trials total, 4 against the sidecar.
- t50 E91 acceptance: L2 data-side profile only; no semantic fields, target joins, L3, reader, mode, or parent assignment. Report, DONE, profile, and diff are retained in v5.
- Framing conflict: t49/t51 match their row records; t50 identity-tail starts match t49 on 251/251 client and 251/251 server rows, while full row spans match on 0/251 and 0/251. No framing winner; t49 field grades unchanged.
- t51 follow-up: Nrvn, Nftb, and Calt records merged with held grades preserved; TCrs/EDfx/EDsc remain open or unresolved.
- L4=0.

## Deliverables

- `reports/club_nation_subtable_schema.json` and `.md`: v5 pair.
- `scratch/t52/out/club_nation_subtable_schema.v4.json` and `.md`: byte-exact v4 baseline snapshots.
- `scratch/t52/out/ledger_snapshot.json`: exact ledger bytes used for the t52 provenance snapshot.
- `scratch/t52/out/consolidate_v5.py`: deterministic builder with `--help` and `--selftest`.
- `scratch/t52/out/verify.py`: independent verifier; it does not import the builder or fm24_dump.
- `scripts/t52_spot_v5.py`: independent 20+ item spot check with `--help` and `--selftest`.
- `scratch/t52/out/spot_*.log`: execution logs.

## Audit Note

The frozen v4 JSON/Markdown hashes are pinned in the builder and verifier. New source-artifact hashes are recorded per task in `incremental_provenance.tasks`. Source tasks, the ledger, and pre-existing worktree changes were read-only.

## fix1

Root cause: build-side provenance was updated to E91 before the validator was updated, leaving a stale `acceptance_ledger_entry is None` guard.
Fix: the validator now requires live E91 to be `acceptance`/`L2` and the t50 scope note to be present, while rejecting t50 attribution in field-grade structures. The L3=0 and `NO WINNER` records are unchanged.
Verification commands were rerun; outputs are appended to `spot_*.log` with the `t52-fix1` marker.
