# Wayfinder v0.1 Architecture

`scanner.py` starts with `Development.manifest.toml`, then follows its registered roots. It recurses only canonical standards, portfolios, and intake roots; reference, infrastructure, and cache roots contribute their direct manifest only. Generated and dependency directories are pruned. It parses records with `tomllib`, retains the manifest location for provenance, and emits diagnostics instead of altering contradictions.

`resolver.py` constructs a context bundle from inherited instructions/manifests, the target manifest and declared read-first records, and registered governing-standard READMEs. `cli.py` presents the same shared result in text or the CTS JSON envelope.

There is no cache, database, network client, daemon, watcher, subprocess execution, or workspace write path.
