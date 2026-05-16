# Caching

Caching stores reused DataFrames or RDDs to avoid recomputation.

Use caching when the same expensive intermediate result is reused multiple times.

Always unpersist data when it is no longer needed.
