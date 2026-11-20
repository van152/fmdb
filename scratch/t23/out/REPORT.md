# t23 nation client status reconciliation

Status: `complete_client_scope_reconciled_with_server_and_schema_coverage_open`. The client row grammar is closed; the 441-field nation ledger is not.

## Reconciled Results

- **Client table_10 framing:** 251 rows; `14 + 24710 + 8 = 24732`; A/B/C/D totals `[492, 214, 63, 162]`; SHA-256 `7e9d740b9ee6900965d8616a136ea4bc54a0f7207f9727eac72badfb727f6c34`.
- **t19 ledger:** status `partial_prefix_cursor_tail_and_loops_unresolved`; its own verifier remains blocked at exit 1; it contains 7/441 named fields. This is consistent with a partial expanded ledger, not a failed g2 row walk.
- **Ncpi:** Ncpi (Capital City) at client body `row+9`, width 4, targeting zero-based city row ordinal; evidence grade `L3`. This is one standalone mapping, not completion of the nation schema.

## Scope Boundaries

- The g2 verifier parses the 2430 client payload only and walks each of the 251 variable rows through identity and footer.
- t01g's original prefix-only negative result remains intact; it did not claim all row starts.
- t19's schema-wide ledger remains partial and its full verifier correctly blocks unresolved row alignment for that ledger.
- No client formula is applied to server table_10; the alternate reader path remains unassigned to client/server.
- The commented Ncpi XML record does not establish current UI editability or L4 behavior.

## Still Open

- Recover a server table_10 grammar and independently close its rows.
- Map the remaining nation fields using helper/branch-aware row coordinates; the current ledger has 434 unnamed entries.
- Reconcile the alternate arg8!=0 reader path with an actual archive before assigning its role.

## Reproduction

`py -V:3.12 -I scratch/t02/inbox/nati/OUTBOX/verify.py --selftest`
`py -V:3.12 -I scripts/t22_nation_capital.py --selftest`
`py -V:3.12 -I scratch/t19/out/verify.py` is expected to report BLOCKED for the expanded t19 ledger.
