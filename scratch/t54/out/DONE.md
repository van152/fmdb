# t54 DONE

- [x] v5/fix1 JSON and Markdown hashes pinned and snapshotted.
- [x] t53 E93 validated as acceptance/L2; no L3 field promotion; L4=0.
- [x] TCrs main and getter vectors recorded as separate EOF-closed members.
- [x] table_extra_9 typed-suffix binding added while preserving t49's six rejection records and t50 source profile.
- [x] t50 NO WINNER string retained as prefix with a separate t53 block-internal note.
- [x] Four PUn* fields remain held; held count stays at 20; eight t53 negative trial groups are listed; negative count is 15.
- [x] Protected v5 sections and all club counters compare equal to the v5 snapshot.
- [x] Builder, verifier, spot script, and t01 anchors passed; see `spot_*.log`.

No game/editor/IDA was launched; no network or Z: access was used.

## fix1
- Root cause: commander recorded E94 (t55 acceptance) after the t54 build, so the 93-entry full-ledger hash/size no longer matched the 94-entry live ledger.
- Fix: builder and verifier now pin only E87/E89/E90/E91/E92/E93 by ID, canonical claim SHA-256, kind, and level; the full-file snapshot remains historical and is not compared with the live ledger.
