# Data directory

Raw NAB files are intentionally not versioned. The empirical runner fetches the frozen series and \`labels/combined_windows.json\` from the upstream NAB repository and caches them under \`data/cache/\`.

The cache is gitignored. Each generated result records SHA-256 hashes of the source files so that the exact upstream bytes used by an experiment can be audited.
