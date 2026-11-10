---
name: dedupe_sources
track: core
kind: local_formatter
requires_env: []
inputs: [items]
outputs: [items, input_count, unique_count, removed_count]
side_effect: false
---

Use this tool to remove repeated sources from a list that already contains URLs.
It keeps the first item for each HTTP(S) URL, including its title, summary, and
other fields. Host case and fragments are ignored. Paths, query parameters, and
the distinction between HTTP and HTTPS are preserved.

For example, `https://example.com/report#intro` and
`https://EXAMPLE.COM/report#methods` produce one item. Two URLs with different
query values stay separate.

An empty list returns zero counts. Invalid input or an invalid URL returns an
error dictionary. The tool runs locally and never reads the URLs.
