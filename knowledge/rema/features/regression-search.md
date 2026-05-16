# Search & Pre-search

<!-- AUTO-EXTRACTED — Do not edit above this line manually -->
<!-- Extracted: 2026-04-01 14:24 | Source: 10 test cases -->

## Overview

Feature area covering 10 test cases. Key areas:
- Pre search Module > Modules load on cold app start
- Pre search Module > Popular products” module is visible
- Pre search Module > Consent is shown if applied
- Pre search Module > Products for you” shown only with consent
- Pre search Module > Recommended Products shown always
- ... and 5 more

## Navigation

- **REG04-01**: Open search screen as logged out user → Open search screen as logged in user
- **REG04-02**: Open search screen
- **REG04-03**: Open search

## UI Elements

| Element | Mentions | Referenced In |
|---------|----------|---------------|
| Open search (screen) | 5 | REG04-01, REG04-02, REG04-04, REG04-05 |
| User is able to add (item) | 2 | REG04-04, REG04-05 |
| User is able to remove (item) | 2 | REG04-04, REG04-05 |
| User is able to check (item) | 2 | REG04-04, REG04-05 |
| detail (screen) | 2 | REG04-04, REG04-05 |
| User is able to swipe to get more (item) | 2 | REG04-04, REG04-05 |
| Popular prodcuts are loaded in the (screen) | 1 | REG04-02 |
| Add to current shopping list from recommended products (carousel) | 1 | REG04-05 |

## Behaviors

### Edge Cases
- **REG04-01**: Pre search Module > Modules load on cold app start
- **REG04-02**: Pre search Module > Popular products” module is visible
- **REG04-03**: Pre search Module > Consent is shown if applied
- **REG04-04**: Pre search Module > Products for you” shown only with consent
- **REG04-05**: Pre search Module > Recommended Products shown always
- **REG04-06**: Search Module > Search works during pre-search loading
- **REG04-07**: Search Module > Typing shows real-time search results
- **REG04-08**: Search Module > Add item from search result
- **REG04-09**: Search Module > Search works if module API fails
- **REG04-10**: Search Module > Item labels & disclaimers work as expected

## API Dependencies

No API endpoints documented in test cases.

## Source Test Cases

- `Regression_Tests/04_search_presearch.txt`
- Total: 10 test cases

<!-- MANUAL — Add your own notes below this line -->

## Manual Notes

<!-- Add accessibility IDs, navigation tips, tricky elements, etc. -->
