# Product Details

<!-- AUTO-EXTRACTED — Do not edit above this line manually -->
<!-- Extracted: 2026-04-01 14:24 | Source: 4 test cases -->

## Overview

Feature area covering 4 test cases. Key areas:
- Open Product Details Page and View Info
- View Product with special labels or restrictions
- Add / Remove product to shopping list
- Add to Favorites/ Remove from favorites

## Navigation

- **REG06-01**: Tap on any product
- **REG06-02**: Open øko product ( search Øko) → Open weight product ( search for selv vej) → Open alcohol  items → Open items wiht max purchase option ( check in newspapers) → Open items with limited availability (check in newspapers) → Open items with discounted price → Open Tobacco items ( search for malboro) → Open private parties items ( search in newspapers) → Open item with multiple labels - search for MINIMÆLK 0,4% ( it has 6 labels)
- **REG06-03**: Tap "+" to add item → Tap "–" to remove item
- **REG06-04**: Open any product → Tap on the heart to favorite an item → Tap on the enabled heart to disable it

## UI Elements

| Element | Mentions | Referenced In |
|---------|----------|---------------|
| Open (item) | 4 | REG06-02 |
| Add to list | 1 | REG06-01 |
| Add to favorites | 1 | REG06-01 |
| Open alcohol (item) | 1 | REG06-02 |
| Open Tobacco (item) | 1 | REG06-02 |
| Open private parties (item) | 1 | REG06-02 |
| Weigh info appears for weighted (item) | 1 | REG06-02 |
| to add (item) | 1 | REG06-03 |
| to remove (item) | 1 | REG06-03 |
| Tap on the heart to favorite an (item) | 1 | REG06-04 |

## Behaviors

### Edge Cases
- **REG06-01**: Open Product Details Page and View Info
  - When: --User is logged in; product is visible in search, shopping list, or catalog
- **REG06-02**: View Product with special labels or restrictions
- **REG06-03**: Add / Remove product to shopping list
- **REG06-04**: Add to Favorites/ Remove from favorites
  - When: --User is logged in

## API Dependencies

No API endpoints documented in test cases.

## Source Test Cases

- `Regression_Tests/06_product_details_page.txt`
- Total: 4 test cases

<!-- MANUAL — Add your own notes below this line -->

## Manual Notes

<!-- Add accessibility IDs, navigation tips, tricky elements, etc. -->
