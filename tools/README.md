# tools/

## leakscan.py

Scans the repo for patterns that should never reach a public repo: infra
identifiers (Notion UUIDs, Supabase project refs), operator identity,
prior product/project names, absolute local paths, live form URLs, generic
PII shapes (emails, institution domains), and secret-shaped strings (API
keys, tokens, passwords).

CI runs it on every push and pull request via
`.github/workflows/leakscan.yml`. The build fails if it finds anything.

Run it locally before pushing:

```
python3 tools/leakscan.py
python3 tools/leakscan.py --verbose   # show full matched text, not masked
python3 tools/leakscan.py --json      # machine-readable output
python3 tools/leakscan.py some/dir    # scan a specific directory instead of repo root
```

### Adding to the denylist

Patterns live in `tools/denylist.txt`, one regex per line, grouped under
`## Section Name` comment headers. A plain `# comment` line immediately
above a pattern becomes its label in scan output. Keep new patterns
structural (regexes matching a *shape*), not literal personal data — see
the next section for where real names/emails go.

### denylist.local.txt (private, never committed)

`tools/denylist.local.txt`, if present, is loaded and merged with
`denylist.txt` at scan time, same format. This is where the operator keeps
a private list of real harvested names and email addresses to scan for —
literal PII that must never be committed to this repo, so it does **not**
belong in `denylist.txt`. Add `tools/denylist.local.txt` to `.gitignore`
and never commit it.

### `tools/denylist.txt` must never contain a literal

`tools/denylist.txt` is committed and public. It ships to everyone who
clones or browses this repo. It exists to catch leaks — if it ever
contains a literal identifier (a real name, a real domain, a real
project ref, a real short-URL code, a codename, a market-fingerprinting
roster) instead of a structural regex, then committing it **is** the
leak: a "denylist of things to catch" that itself contains the thing it's
supposed to catch defeats its own purpose and publishes exactly the data
it exists to protect. Any repo derived from a private operation carries
this risk by default — the denylist is drafted by someone who has the
real identifiers in front of them, so it's easy to paste one in instead
of generalizing it into a pattern. This check exists to make that mistake
unpublishable rather than relying on the drafter to never make it.

`leakscan.py` skips its own denylist files when scanning for hits
(`SELF_SKIP_BASENAMES`), which means the normal scan cannot catch a
literal placed in `denylist.txt` — it would need the literal to already
be in the denylist to flag it, and skips the file it's in anyway. To
close that blind spot, every run of `leakscan.py` separately checks
whether any non-comment line in the public `denylist.txt` also appears,
verbatim, as a non-comment line in the private `denylist.local.txt`. A
match means someone copied a literal from the private list into the
public one, and the scan fails immediately with the offending line(s)
before doing anything else. If you hit this: move the line from
`denylist.txt` to `denylist.local.txt`, and if it was already pushed,
treat it as a real leak (rewrite history, rotate any credential it
exposed).

## validate.py

A forker-facing setup linter, not a leak scanner. Run it after forking to
see what's left to configure:

```
python3 tools/validate.py
python3 tools/validate.py --strict   # exit 1 if anything is unfilled
```

It reports which of the five `brain/*.md` market files are still unfilled,
whether `active-focus/focus.md` is filled, and any remaining
`<PLACEHOLDER_TOKEN>` markers across the repo, grouped by file. Exits 0
always unless `--strict` is passed — it's informational, meant to point a
new forker at what to fill in next.
