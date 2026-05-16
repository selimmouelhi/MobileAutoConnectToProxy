Search for **all bugs** in **Ready for QA** status in the FRA project on `vigotech.atlassian.net`, across all fix versions.

**Project:** FRA
**Status filter:** Ready for QA
**Issue type:** Bug

**Output format** — group by fix version, starting from the newest (unreleased first, then released in reverse order, then no fix version last). Use exactly this clean format:

```
## Bugs in Ready for QA

### [Version name]
- [Bug title](https://vigotech.atlassian.net/browse/KEY)
- [Bug title](https://vigotech.atlassian.net/browse/KEY)

### [Version name]
- [Bug title](https://vigotech.atlassian.net/browse/KEY)

### No fix version
- [Bug title](https://vigotech.atlassian.net/browse/KEY)
```

Keep it minimal: just the title as a link. No tables, no priority, no assignee, no extra details unless I ask.

If there are no bugs, just say "No bugs in Ready for QA".
