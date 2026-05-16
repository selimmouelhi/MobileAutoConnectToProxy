# Bug Report Template

## About This Template

This template defines the standard bug report format currently used in Jira across our projects. It serves as the reference for building the equivalent bug template in Notion.

### How to read this template
- Fields and sections marked with `*` are **required** — they must be filled in for every bug.
- Fields without `*` are **optional** — fill them in when relevant, but they can be left empty.
- Placeholders (e.g. `e.g. 1.0.0`, `X.X.X`) show the expected format — replace them with actual values.
- `<!-- comments -->` are instructions for the person filling in the bug — they should not appear in the final report.

### Field reference

| Field | Required | Type | Allowed Values |
|-------|----------|------|----------------|
| **Title** | * | Text | Short, clear bug summary |
| **Component** | * | Single select | Project-specific (e.g. `Mobile`, `Backend`) |
| **Found in version** | * | Version | Version from the project's release list |
| **Found in build** | * | Number/label | Build number, e.g. `85` |
| **Testing Configuration** | * | Text block | Device, OS, environment, and test account (see format below) |
| **Steps to Reproduce** | * | Numbered list | Step-by-step instructions to trigger the bug |
| **Expected Result** | * | Text | What should happen |
| **Actual Result** | * | Text | What actually happens |
| **Priority** | | Single select | `Urgent` \| `High` \| `Medium` \| `Low` (defaults to Medium) |
| **Severity** | | Single select | `High` \| `Medium` \| `Low` (defaults to Not set) |
| **Reproducibility** | | Single select | `High` \| `Low` \| `Unknown` \| `Cannot Reproduce` |
| **Parent Epic** | | Issue link | Link to related epic/feature |
| **Attachments** | | Files | Screenshots, screen recordings |

---

## Template

### [Title] *
<!-- Short, clear bug summary — this becomes the page title -->

| Field | Value |
|-------|-------|
| **Component** * | |
| **Found in version** * | |
| **Found in build** * | |
| **Priority** | |
| **Severity** | |
| **Reproducibility** | |
| **Parent Epic** | |

### Testing Configuration *
<!-- Include: app version + build number, device + OS, environment, test account -->

> version X.X.X #XX
> Device - OS version
> Environment (Inhouse / Production)
> Test account used

### Steps to Reproduce *
1.
2.
3.

### Expected Result *
-

### Actual Result *
-

### Attachments
<!-- Screenshots, screen recordings -->
