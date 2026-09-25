# Data directory

Raw NAB files are intentionally not versioned. The empirical runner fetches the selected streams and `labels/combined_windows.json` from frozen NAB revision `ea702d75cc2258d9d7dd35ca8e5e2539d71f3140` and caches them under `data/cache/`.

The cache is gitignored, but cached files are not trusted blindly: every empirical run verifies annotation and series bytes against the frozen SHA-256 values documented in `DATA.md`. A mismatch stops the study and requires an explicit protocol revision.
