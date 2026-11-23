# t96b Unicorn closure — partial

No new full-table Unicorn pass was completed in this run. The existing t96 artifact is the sole measurement source; its failures are not promoted to successes.

- Expected archive/table pairs: 79 inventoried archive/table combinations.
- Pairs present in source artifact: 79.
- Pairs marked closed in source: 0.
- `table_9`: prior artifact reports server 5 successful rows (then unmapped read) and client failure at row 0; neither closed.
- `table_10`: prior artifact reports only row 0 attempted and unsuccessful for both archives.
- No verified findings on polymorphic prefix flags or constructors; these remain unresolved.
- The required four-table diff=0 selftest and 251-row table9/table10 closures were not achieved.

Failure diagnostics and field aggregates are carried over only when present in the prior source. No row-level raw reads are stored.
