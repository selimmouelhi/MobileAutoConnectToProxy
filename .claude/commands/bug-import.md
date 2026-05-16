Import bug **$ARGUMENTS** from Jira and create a local markdown file.

## Steps

### 1. Fetch from Jira

Call `getJiraIssue` with:
- **cloudId**: `e29cf11b-900b-42fd-940d-3b56fd143dba`
- **issueKey**: `$ARGUMENTS`

Retrieve fields: summary, status, priority, fixVersions, components, description (ADF), created.

### 2. Parse the ADF description

The description is in Atlassian Document Format. Extract:

- **Info panel** → contains build info, device/platform, environment (each on a separate line via `hardBreak`)
- **Ordered list** after "Steps to reproduce" heading → numbered steps
- **Bullet list** after "Actual Result" heading → actual result items
- **Bullet list** after "Expected Result" heading → expected result items

For each ADF node, walk the `content` array recursively and extract text. Handle these node types:
- `panel` with `attrs.panelType: "info"` → info panel
- `orderedList` → steps
- `bulletList` → result items
- `paragraph` with bold text → section headers

### 3. Determine directory path

Extract the fix version:
- If `fixVersions` is non-empty, use the **first** version's `name` field
- Extract just the version number (e.g., "6.6.1" from "6.6.1 (Favorite recipes)")
- Directory: `bugs/FRA/<version>/`
- If no fix version exists, use `bugs/FRA/unversioned/`

### 4. Check for existing file

Glob for `bugs/FRA/*/$ARGUMENTS.md`:
- If found, ask the user: *"File already exists at `<path>`. Overwrite or skip?"*
- If not found, proceed

### 5. Create the markdown file

Create directories as needed, then write the file using this template:

```markdown
---
jira_key: <key>
jira_url: https://vigotech.atlassian.net/browse/<key>
project: FRA
summary: "<summary - quote if contains special chars>"
status: <status name>
priority: <priority name>
fix_version: "<version number or empty>"
components:
  - <component names>
platform: <iOS or Android - infer from components>
device: "<extracted from info panel or empty>"
os_version: "<extracted from info panel or empty>"
build: "<extracted from info panel or empty>"
environment: <extracted from info panel, default Preprod>
created: <issue created date, YYYY-MM-DD>
imported: <today's date, YYYY-MM-DD>
---

# <key>: <summary>

## Steps to Reproduce
1. <step 1>
2. <step 2>
...

## Expected Result
- <expected item>

## Actual Result
- <actual item>

## Verification
| Field | Value |
|-------|-------|
| Status | not_verified |
| Date | |
| Agent | |
| Result | |

### Agent Notes


### Screenshots

```

### 6. Report

Print: `Imported $ARGUMENTS -> bugs/FRA/<version>/$ARGUMENTS.md`

Then suggest: *"Run `/bug-read $ARGUMENTS` to view or `/bug-verify $ARGUMENTS` to verify via Appium."*

## Parsing guidelines

- If the ADF is missing sections (e.g., no expected result), leave those sections empty in the markdown
- If the info panel doesn't have all 3 lines, extract what's available
- Strip any trailing whitespace from extracted text
- For the `platform` field: if components include "iOS" → `iOS`, if "Android" → `Android`, if both → `iOS, Android`
- For `device` and `os_version`: parse from the info panel second line (e.g., "iPhone 16 Pro - iOS 18" → device: "iPhone 16 Pro", os_version: "iOS 18")
