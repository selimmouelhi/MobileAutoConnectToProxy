# App Install & Update

<!-- AUTO-EXTRACTED — Do not edit above this line manually -->
<!-- Extracted: 2026-04-01 14:24 | Source: 7 test cases -->

## Overview

Feature area covering 7 test cases. Key areas:
- App install > Install RC build
- App install > Install RC build and observe onboarding
- App install > Reinstall RC build after deletion
- App update > Update the public app
- App update > Update the app while logged in
- ... and 2 more

## Navigation

- **REG01-01**: Open the app
- **REG01-04**: Open the app → Tap on order button

## UI Elements

| Element | Mentions | Referenced In |
|---------|----------|---------------|
| Add (item) | 2 | REG01-03, REG01-07 |
| User is able to add (item) | 1 | REG01-01 |
| s to current shopping list or browse different (item) | 1 | REG01-01 |
| Add a list and add (item) | 1 | REG01-04 |
| Tap on order (button) | 1 | REG01-04 |
| Make sure to have (item) | 1 | REG01-07 |
| same (item) | 1 | REG01-07 |

## Behaviors

### Edge Cases
- **REG01-01**: App install > Install RC build
- **REG01-02**: App install > Install RC build and observe onboarding
- **REG01-03**: App install > Reinstall RC build after deletion
- **REG01-04**: App update > Update the public app
  - When: --user is not logged in
- **REG01-05**: App update > Update the app while logged in
  - When: --user is logged in
- **REG01-06**: App update > Update the app while having an ongoing order
- **REG01-07**: App update > Update the app while having items in favorites to the newest version

## API Dependencies

No API endpoints documented in test cases.

## Source Test Cases

- `Regression_Tests/01_app_install_update.txt`
- Total: 7 test cases

<!-- MANUAL — Add your own notes below this line -->

## Manual Notes

<!-- Add accessibility IDs, navigation tips, tricky elements, etc. -->
