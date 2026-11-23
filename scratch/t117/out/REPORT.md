# t117 Big-3 gap closure audit

Result: **0 of 294 gaps upgraded**. This is intentional: available evidence does not provide the required per-4CC destination provenance. The denominator remains 1,034; coverage remains 379/1,034 gross (36.7%) and 379/673 net (56.3%).

## Findings and blockers
- The `gap_off_not_in_read_stream` classification cannot be resolved from table-level trace summaries. A valid upgrade requires a concrete Unicorn write address and `mem_off`, joined to the corresponding accessor/4CC.
- All 21 table_45 child candidates have `mem_off=null` in the t109 handler route. t98 gives 18 physical columns and 117 accessors, but no proven crosswalk from those rows to these 21 tags. They remain unresolved rather than being guessed.
- Helper/delegate/other-table rows remain unresolved absent exact persisted-field proof. The generated JSON retains each row, its old evidence and a category-specific next step.
- `t105 --selftest` failure diagnosis: its `steps("NTC::server")` lookup raises KeyError because the serialized function key is `NATIONAL_TEAM_CONTAINER::server` (see `scratch/t105/out/big3_serializers.json` `functions` keys); test label/key alias is inconsistent. No t105 source was modified.

## Verification
All 1,034 t109 rows are conserved with unchanged classes. No evidence was promoted to L3/exclusion.
