Reject the bug **$ARGUMENTS** in the FRA project on `vigotech.atlassian.net`.

**Arguments format:** `FRA-XXXX "reason for rejection"`
- First argument ($1): The bug key (e.g., FRA-1234)
- Remaining arguments: The rejection reason

**Steps to execute:**
1. First, fetch the bug to confirm it exists and show its title
2. Check if the bug has a fix version set — if not, you MUST set one before transitioning (Jira requires it for rejection)
3. Add a comment to the bug with the rejection reason, formatted as:

```
**Rejected by QA**

Reason: [the reason provided]
```

4. Transition the bug to **Rejected** status (find the correct transition ID using getTransitionsForJiraIssue)
5. Confirm the action

**Output format:**

```
Rejected [FRA-XXXX](https://vigotech.atlassian.net/browse/FRA-XXXX) — [bug title]
Reason: [reason]
```

If the transition fails or the bug can't be rejected from its current status, explain why and suggest what to do instead.
