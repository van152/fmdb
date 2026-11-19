# t46 DONE

- Scope: server table_10 data-side only; no game/editor/IDA/network access.
- Server table_10 present; 251 identity-framed rows; `14 + sum(row_lens=422323) + 8 = 422345`.
- Client payload/cursor consumed for comparison only; no client rows redumped.
- Whole-row grammar comparison: different; server A/B/C/D internals remain unknown.
- L1: payload/frame, row framing, closure, and byte profiles; L2: all row ordinals/IDs cross-match t25.
- New L3 claims: 0; L4: 0.
- Required verification commands are recorded in REPORT.md.
