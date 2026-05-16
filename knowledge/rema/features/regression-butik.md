# Butik (Virtual Store)

<!-- AUTO-EXTRACTED — Do not edit above this line manually -->
<!-- Extracted: 2026-04-01 14:24 | Source: 3 test cases -->

## Overview

Feature area covering 3 test cases. Key areas:
- Browse and Search Shop Items
- Add and Remove Products from Shopping List
- View Product Details and Add from Detail View

## Navigation

- **REG07-01**: Open Butik tab → Tap on a category → View sub-category list
- **REG07-03**: Tap on a product to open the Product Details screen → Open øko product ( search Øko) → Open weight product ( search for selv vej) → Open alcohol  items → Open items wiht max purchase option ( check in newspapers) → Open items with limited availability (check in newspapers) → Open items with disconted price → Open Tobacco items ( search for malboro) → Open private parties items ( search in newspapers) → Open item with multiple labels - search for MINIMÆLK 0,4% ( it has 6 labels) → Tap add ot the shopping list

## UI Elements

| Element | Mentions | Referenced In |
|---------|----------|---------------|
| Open (item) | 4 | REG07-03 |
| Open Butik (tab) | 1 | REG07-01 |
| Swipe through categories or use grid (selector) | 1 | REG07-01 |
| Use the search (bar) | 1 | REG07-01 |
| Swipe right to add an (item) | 1 | REG07-02 |
| Swipe left to remove the same (item) | 1 | REG07-02 |
| Check the total price and (item) | 1 | REG07-02 |
| In app notification is shown while adding (item) | 1 | REG07-02 |
| Tap on a product to open the Product Details (screen) | 1 | REG07-03 |
| Open alcohol (item) | 1 | REG07-03 |
| Open Tobacco (item) | 1 | REG07-03 |
| Open private parties (item) | 1 | REG07-03 |
| Go back and confirm (item) | 1 | REG07-03 |
| Weigh info appears for weighted (item) | 1 | REG07-03 |

## Behaviors

### Edge Cases
- **REG07-01**: Browse and Search Shop Items
  - When: --user is logged in or guest
- **REG07-02**: Add and Remove Products from Shopping List
  - When: --Product list is visible
- **REG07-03**: View Product Details and Add from Detail View

## API Dependencies

No API endpoints documented in test cases.

## Source Test Cases

- `Regression_Tests/07_butik_virtual_store.txt`
- Total: 3 test cases

<!-- MANUAL — Add your own notes below this line -->

## Manual Notes

<!-- Add accessibility IDs, navigation tips, tricky elements, etc. -->
