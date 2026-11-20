# t52 DONE

- [x] v4 baseline frozen and SHA-256 verified.
- [x] t47/t49/t50/t51 source artifacts SHA-256 recorded.
- [x] v4 protected content retained; nation increments appended.
- [x] t50 L1/L2 profile merged without semantic-field promotion.
- [x] t49/t50 framing conflict represented as two alternatives; no winner selected.
- [x] t50 sidecar candidate retained as unassigned; negative findings preserved.
- [x] t51 cross-walk and follow-up field grades merged.
- [x] Coverage totals generated: 30 L3 / 30 unique / 20 held / 7 bounded negative records.
- [x] Help, selftests, build, independent verification, spot checks, and t01 anchors passed; see `spot_*.log`.

L4=0. No game/editor/IDA process was launched; no network access was used.

## fix1

Root cause: the builder began emitting E91 provenance before the schema validator was updated, so build and validation disagreed about the t50 acceptance entry.
Fix: validation now requires live E91 to be an `acceptance`/`L2` entry with the t50 ledger scope note, while separately rejecting any t50 attribution in field-grade structures. t50 remains L3=0.
E92 records the t52 fix1 acceptance at L2; E91 remains the t50 L2-only entry. Runtime results are recorded in the appended `spot_*.log` entries marked `t52-fix1`.
