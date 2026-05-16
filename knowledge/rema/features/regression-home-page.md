# Home Page

<!-- AUTO-EXTRACTED — Do not edit above this line manually -->
<!-- Extracted: 2026-04-01 14:24 | Source: 10 test cases -->

## Overview

Feature area covering 10 test cases. Key areas:
- App loads front page and renders all modules
- Shopping list module diplays items
- Favorites module display items
- Aviser module displays items
- Info box is displayed with correct variant
- ... and 5 more

## Navigation

- **REG03-01**: Open app as logged out user
- **REG03-04**: Tap on a magazine → Tap on item → Tap on all items → Tap on avisvarer
- **REG03-06**: As logged out users open front page → As logged in user open front page → OPen search from global search or inside shopping list detail page
- **REG03-07**: As logged in user open front page → OPen search from global search or inside shopping list detail page
- **REG03-08**: Open front page
- **REG03-09**: Tap to accept consent

## UI Elements

| Element | Mentions | Referenced In |
|---------|----------|---------------|
| User is able to add (item) | 3 | REG03-04, REG03-06, REG03-07 |
| User is able to remove (item) | 2 | REG03-06, REG03-07 |
| User is able to swipe to get more (item) | 2 | REG03-06, REG03-07 |
| inspirational (shelf) | 1 | REG03-01 |
| Favorites (carousel) | 1 | REG03-03 |
| User is able to add / remove (item) | 1 | REG03-03 |
| User is able to unheart (item) | 1 | REG03-03 |
| User is able to see all favorites from (icon) | 1 | REG03-03 |
| or all (item) | 1 | REG03-03 |
| s in the (carousel) | 1 | REG03-03 |
| Browse (item) | 1 | REG03-04 |
| Tap on (item) | 1 | REG03-04 |
| Tap on all (item) | 1 | REG03-04 |
| Aviser (carousel) | 1 | REG03-04 |
| User is able to browse all (item) | 1 | REG03-04 |
| and upcoming with disabled (item) | 1 | REG03-04 |
| User is able to see full list (view) | 1 | REG03-04 |
| of avisvarer with all (item) | 1 | REG03-04 |
| User is able to favorite (item) | 1 | REG03-06 |

## Behaviors

### Edge Cases
- **REG03-02**: Shopping list module diplays items
- **REG03-03**: Favorites module display items
  - When: User is logged in
- **REG03-04**: Aviser module displays items
- **REG03-05**: Info box is displayed with correct variant
- **REG03-06**: Popular products
- **REG03-07**: Inspirational products
- **REG03-08**: Consent Module > Consent UI rendring
- **REG03-09**: Consent Module > Consent Action
- **REG03-10**: Order card is shown

### Error States
- **REG03-01**: App loads front page and renders all modules
  - Expected: App launches to front page; Content loads correctly from backend; A new shopping list is created and selected ( 0 items) for logged out users

## API Dependencies

No API endpoints documented in test cases.

## Source Test Cases

- `Regression_Tests/03_home_page.txt`
- Total: 10 test cases

<!-- MANUAL — Add your own notes below this line -->

## Manual Notes

<!-- Add accessibility IDs, navigation tips, tricky elements, etc. -->
