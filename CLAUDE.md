# QA-Rema — Claude Code Instructions

## Who I Am

Selim Mouelhi — QA Engineer working on the **Rema 1000** mobile app (iOS & Android).
Daily work: bug filing, triage, test case writing, bug verification (manual + Appium automation), release management, and building test automation.

## Projects

| Project | Instance | Key | What |
|---------|----------|-----|------|
| **FRA** (primary) | vigotech.atlassian.net | FRA | Rema 1000 grocery app — iOS & Android |
| **ShapeHQ** | shapedk.atlassian.net | STP | STEF TEST PROJECT — secondary/testing workspace |

## Behavior Preferences

- **Be concise** — I know the context, don't over-explain
- **Skip confirmations** — When I say "create bug" or "post", just do it. Don't ask "are you sure?"
- **Danish context** — The Rema app is in Danish. Always consider Danish labels, button text, and UI strings in bugs, test cases, and Appium automation
- **Proactive suggestions** — When you notice an opportunity to use a relevant command or skill, suggest it
- **Bugs are always unassigned** — Never set an assignee when creating Jira bugs
- **Full test case previews** — When showing test cases, always show full content (Preconditions, Actions, Expected, API), never just titles

## Available Skills & Commands

### Skills (invoke with `/skill-name`)
| Skill | When to suggest |
|-------|----------------|
| `/bug-verify FRA-XXXX` | After importing a bug, or when I mention verifying/reproducing a bug |
| `/knowledge-update` | When test case files change, or before bug verification if knowledge might be stale |

### Commands (invoke with `/command-name`)
| Command | When to suggest |
|---------|----------------|
| `/bugs-current` | Start of a QA session — see what's ready for testing |
| `/bugs-mine` | Check my assigned bugs |
| `/bugs-all` | Full bug list for current release |
| `/bug-import FRA-XXXX` | Before `/bug-verify` — imports bug locally for automation |
| `/bug-read FRA-XXXX` | Quick view of a local bug file |
| `/bug-summary` | During release prep — overview of all bugs |
| `/release-status` | Release readiness check |
| `/test-report` | Generate test execution report for current release |
| `/reject-bug FRA-XXXX` | When a bug should be rejected (transitions in Jira) |

### Agents (used automatically)
| Agent | Triggered by |
|-------|-------------|
| **jira-bug-reporter** | "create bug", "file bug", or any bug description with project context |
| **rema-app-expert** | Questions about app screens, navigation, UI elements, APIs, feature flags |
| **testpad-casecrafter** | "write test cases", "create tests for", or test case requests from specs |

## Typical Workflows

### Bug Triage Session
1. `/bugs-current` — See bugs in Ready for QA
2. Pick a bug → `/bug-import FRA-XXXX`
3. `/bug-verify FRA-XXXX` — Automated reproduction via Appium
4. If not reproducible → `/reject-bug FRA-XXXX`

### Bug Filing
- Just describe the bug naturally (even briefly) → jira-bug-reporter handles the rest
- Always mention the **version** (e.g., "in 6.6.1") and **platform** if relevant

### Test Case Writing
- Share a spec, Notion link, or feature description → testpad-casecrafter generates structured test cases
- Test cases follow TestPad format: `MODULE-NN | Title [Priority]` with Preconditions/Actions/Expected/API sections

### Release Check
1. `/release-status` — Quick overview
2. `/bug-summary` — Detailed bug breakdown
3. `/test-report` — Cross-reference Jira data with test execution

## Knowledge Systems

- **Knowledge base** (`knowledge/rema/`) — Extracted from 469+ test cases. Covers screens, navigation, elements, APIs, feature flags
- **Test case RAG** (`testcase-rag/`) — 1,939 indexed test cases (Rema + Norlys) in ChromaDB for semantic search
- Run `/knowledge-update` to refresh after test case changes

## Key Directories

```
bugs/FRA/<version>/       — Local bug markdown files (for automation)
testcases/Rema/           — Source test case files (14+ modules)
knowledge/rema/           — Extracted app knowledge (auto-generated)
testcase-rag/             — RAG system + ChromaDB index
appium-tests/             — WebDriverIO/Mocha framework (reference, not integrated)
proxyman-scripts/         — API mock scripts
```
