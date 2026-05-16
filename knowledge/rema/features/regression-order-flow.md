# Order Flow

<!-- AUTO-EXTRACTED — Do not edit above this line manually -->
<!-- Extracted: 2026-04-01 14:24 | Source: 3 test cases -->

## Overview

Feature area covering 3 test cases. Key areas:
- Start and Complete a Køb & Hent Order [TO TEST ON PREPROD]
- Order Status and Interactions [TO TEST ON PREPROD]
- Orders History [TO TEST ON PREPROD]

## Navigation

- **REG09-01**: Start order flow via K&H by tapping on order button → Tap continue
- **REG09-02**: Go to front page → Tap current order to view details
- **REG09-03**: Open an order that has expired → Open an ongoain order but not picked up yet → Open an ongoain order and picked up → Open an order that has been marked done and rated → Open an order that has been marked as done but not rated

## UI Elements

| Element | Mentions | Referenced In |
|---------|----------|---------------|
| Add a mix of standard products and unspecified (item) | 1 | REG09-01 |
| Add alcohol to the (item) | 1 | REG09-01 |
| H by tapping on order (button) | 1 | REG09-01 |
| Order receipt matches all listed (item) | 1 | REG09-01 |
| Tap current order to (view) | 1 | REG09-02 |

## Behaviors

### Edge Cases
- **REG09-01**: Start and Complete a Køb & Hent Order [TO TEST ON PREPROD]
  - When: --User is logged in with items in shopping list
- **REG09-03**: Orders History [TO TEST ON PREPROD]
  - When: --User has already past orders

### Error States
- **REG09-02**: Order Status and Interactions [TO TEST ON PREPROD]
  - Expected: Order banner is visible and updates based on progress; Delivery info is correct (time, items, cost); After order is taken, the order cannot be cancele

## API Dependencies

No API endpoints documented in test cases.

## Source Test Cases

- `Regression_Tests/09_order_flow_preprod.txt`
- Total: 3 test cases

<!-- MANUAL — Add your own notes below this line -->

## Manual Notes

<!-- Add accessibility IDs, navigation tips, tricky elements, etc. -->
