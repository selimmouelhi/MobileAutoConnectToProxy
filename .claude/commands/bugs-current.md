Search for bugs in **Ready for QA** status in the FRA project on `vigotech.atlassian.net`.

**Arguments:** $ARGUMENTS

**Step 1 — Determine the fix version:**
- If `$ARGUMENTS` contains a version (e.g. "6.6.1", "6.7"), use that directly as the fix version filter.
- If `$ARGUMENTS` is empty or doesn't contain a version, **ask the user** which fix version they want to check. Do NOT run a broad discovery query.

**Step 2 — Query bugs:**
Once you have the version, run a single JQL query:
```
project = FRA AND issuetype = Bug AND status = "Ready for QA" AND fixVersion = "<version>"
```
Only request fields: `summary`

**Output format** — use exactly this clean format, nothing else:

```
## Bugs in Ready for QA — [version name]

- [Bug title](https://vigotech.atlassian.net/browse/KEY)
- [Bug title](https://vigotech.atlassian.net/browse/KEY)
```

Keep it minimal: just the title as a link. No tables, no priority, no assignee, no extra details unless I ask.

If there are no bugs, just say "No bugs in Ready for QA for [version]".
