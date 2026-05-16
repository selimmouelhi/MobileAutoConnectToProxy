Generate a **test execution report** for the current release by cross-referencing Jira bug data from the FRA project on `vigotech.atlassian.net`.

**How to find the current version:**
1. First, search for bugs with no fixVersion filter to discover which fix versions exist
2. Identify the **earliest unreleased** fix version — that's the current release

**Project:** FRA
**Fix version:** Current unreleased version (discovered above)

**What to do:**
1. Fetch all bugs in the current fix version
2. Calculate the following metrics from the bug data

**Output format** — use exactly this clean format:

```
## Test Report — [version name]

### Bug Metrics
- **Total bugs filed:** X
- **Verified (Done):** X
- **Rejected:** X
- **Still in QA:** X (Ready for QA)
- **Awaiting fix:** X (In Progress / To Do / Open)
- **Pass rate:** X% (Done / Total)
- **Rejection rate:** X% (Rejected / Total)

### Bug Breakdown by Component
| Component | Total | Done | Rejected | Open |
|-----------|-------|------|----------|------|
| iOS | X | X | X | X |
| Android | X | X | X | X |
| Backend | X | X | X | X |

### Bugs Still Open
- [Bug title](https://vigotech.atlassian.net/browse/KEY) — [status] — [assignee]

### Verdict
[Based on the numbers: is this release ready for sign-off? State clearly: "Release looks good" if all bugs are Done/Rejected, or "X bugs still open — not ready for release" if bugs remain]
```

Skip sections that have no data. Keep it factual and concise.
