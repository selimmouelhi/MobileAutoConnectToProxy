Generate a **bug summary** for the current release in the FRA project on `vigotech.atlassian.net`.

**How to find the current version:**
1. First, search for bugs with no fixVersion filter to discover which fix versions exist
2. Identify the **earliest unreleased** fix version — that's the current release

**Project:** FRA
**Issue type:** Bug
**Fix version:** Current unreleased version (discovered above)

**What to fetch:**
Search for ALL bugs in the current fix version (no status filter) and group them by status.

**Output format** — use exactly this clean format, nothing else:

```
## Bug Summary — [version name]

**Total:** X bugs

### By Status
- Ready for QA: X
- In Progress: X
- Done: X
- Rejected: X
- [other statuses]: X

### Ready for QA
- [Bug title](https://vigotech.atlassian.net/browse/KEY) — assigned to [name]

### In Progress
- [Bug title](https://vigotech.atlassian.net/browse/KEY) — assigned to [name]

### Done / Rejected
- [Bug title](https://vigotech.atlassian.net/browse/KEY) — [Done/Rejected]
```

Skip any status group that has 0 bugs. Keep it concise — this is for standup/reports.
