Read and display the local bug file for **$ARGUMENTS**.

**Steps:**

1. Search for the bug file using glob pattern `bugs/FRA/*/$ARGUMENTS.md`
2. If found, read the file and display its full contents (frontmatter + body)
3. Parse the YAML frontmatter and show a quick status summary:
   - Jira key, summary, status, priority, fix version
   - Verification status (from the Verification table)
4. If the Verification status is `not_verified`, suggest: *"Run `/bug-verify $ARGUMENTS` to verify this bug via Appium."*
5. If no file is found, report: *"No local bug file found for $ARGUMENTS. Run `/bug-import $ARGUMENTS` to import it from Jira."*
