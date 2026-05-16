# Pre-Defined Products

<!-- AUTO-EXTRACTED — Do not edit above this line manually -->
<!-- Extracted: 2026-04-01 14:24 | Source: 20 test cases -->

## Overview

Feature area covering 20 test cases. Key areas:
- Verify pre-defined product shelf displays on front page
- Verify pre-defined product shelf displays on pre-search screen
- Verify "Se alle" opens product list page
- Verify back navigation from "Se alle" page
- Verify tapping a product in the carousel opens product details
- ... and 15 more

## Navigation

- **PREDEF-01**: User is on the front page (home screen)
- **PREDEF-02**: User is on the search screen before entering any search query → Tap the search bar to enter pre-search view
- **PREDEF-03**: User is on front page or pre-search → Tap the "Se alle" button on the pre-defined product shelf
- **PREDEF-04**: User has opened the "Se alle" page from the pre-defined product shelf → Tap the back button
- **PREDEF-05**: Tap on a product card in the pre-defined product shelf carousel
- **PREDEF-06**: User has tapped a product in the pre-defined shelf and is on the product details screen → Tap the back button
- **PREDEF-07**: Tap the add button on a product in the pre-defined shelf carousel
- **PREDEF-08**: User has opened the "Se alle" page from pre-defined product shelf → Tap the add button on a product in the list
- **PREDEF-09**: Tap the add button on the same product in the carousel
- **PREDEF-10**: Navigate to front page and observe the pre-defined shelf

## UI Elements

| Element | Mentions | Referenced In |
|---------|----------|---------------|
| Se alle | 6 | PREDEF-01, PREDEF-02, PREDEF-03, PREDEF-15, PREDEF-17 |
| pre-defined product (shelf) | 5 | PREDEF-01, PREDEF-02, PREDEF-04, PREDEF-06, PREDEF-13 |
| Tap the add (button) | 3 | PREDEF-07, PREDEF-08, PREDEF-09 |
| android_predefined_products | 3 | PREDEF-07, PREDEF-08, PREDEF-09 |
| ios_predefined_products | 3 | PREDEF-07, PREDEF-08, PREDEF-09 |
| Observe the pre-defined product (shelf) | 3 | PREDEF-11, PREDEF-15, PREDEF-18 |
| Tap the search (bar) | 2 | PREDEF-02, PREDEF-13 |
| Tap the back (button) | 2 | PREDEF-04, PREDEF-06 |
| User returns to the previous (screen) | 2 | PREDEF-04, PREDEF-06 |
| Add (button) | 2 | PREDEF-07, PREDEF-08 |
| products | 2 | PREDEF-16 |
| The (shelf) | 2 | PREDEF-18, PREDEF-20 |
| Locate the pre-defined product (shelf) | 1 | PREDEF-01 |
| shelf uses the same (carousel) | 1 | PREDEF-01 |
| shelf title from Contentful is displayed above the (carousel) | 1 | PREDEF-01 |
| Products are shown in a horizontal scrollable (carousel) | 1 | PREDEF-01 |
| to enter pre-search (view) | 1 | PREDEF-02 |
| Scroll to locate the pre-defined product (shelf) | 1 | PREDEF-02 |
| is displayed on the pre-search (screen) | 1 | PREDEF-02 |
| button on the pre-defined product (shelf) | 1 | PREDEF-03 |
| All products from the (shelf) | 1 | PREDEF-03 |
| Page title matches the (shelf) | 1 | PREDEF-03 |
| Tap on a product card in the pre-defined product (shelf) | 1 | PREDEF-05 |
| Product details (screen) | 1 | PREDEF-05 |
| on a product in the pre-defined (shelf) | 1 | PREDEF-07 |

## Behaviors

### Normal Flow (P0/P1)
- **PREDEF-01** [P0]: Verify pre-defined product shelf displays on front page
  - Expected: The pre-defined product shelf is displayed on the front page; The shelf uses the same carousel UI as popular products; The shelf title from Contentful
- **PREDEF-02** [P0]: Verify pre-defined product shelf displays on pre-search screen
  - Expected: The pre-defined product shelf is displayed on the pre-search screen; Same products, title, and layout as on the front page; "Se alle" button is visibl
- **PREDEF-03** [P0]: Verify "Se alle" opens product list page
  - Expected: Product list page opens; All products from the shelf are displayed; Page title matches the shelf title from Contentful
- **PREDEF-04** [P1]: Verify back navigation from "Se alle" page
  - Expected: User returns to the previous screen (front page or pre-search); The pre-defined product shelf is still visible; Shelf content and scroll position are 
- **PREDEF-05** [P0]: Verify tapping a product in the carousel opens product details
  - Expected: Product details screen opens for the selected product; Product information (name, price, image) is displayed
- **PREDEF-06** [P1]: Verify back navigation from product details to shelf
  - Expected: User returns to the previous screen (front page or pre-search); The pre-defined product shelf is still visible; Carousel scroll position is preserved
- **PREDEF-07** [P0]: Verify adding product to shopping list from carousel uses correct source
  - Expected: Product is added to the shopping list; Shopping list source is "android_predefined_products" (Android) or "ios_predefined_products" (iOS); Add button 
- **PREDEF-08** [P0]: Verify adding product to shopping list from "Se alle" page uses correct source
  - Expected: Product is added to the shopping list; Shopping list source is "android_predefined_products" (Android) or "ios_predefined_products" (iOS); Add button 
- **PREDEF-09** [P1]: Verify adding a product already in shopping list increments quantity
  - Expected: Product quantity increments in the shopping list; Shopping list source remains "android_predefined_products" (Android) or "ios_predefined_products" (i
- **PREDEF-10** [P1]: Verify all users see the same products (not personalized)
  - Expected: Both users see the exact same products in the same order; No personalization is applied based on user behavior or history

### Edge Cases
- **PREDEF-12** [P2]: Verify no reload within 1-hour window
  - When: User has loaded the front page with the pre-defined product shelf; Less than 1 hour has passed since the initial load
- **PREDEF-15** [P2]: Verify shelf displays correctly with single product
  - When: Content editors have configured a pre-defined shelf with exactly 1 product
- **PREDEF-18** [P2]: Verify no loading state is shown
  - When: App is freshly launched
- **PREDEF-19** [P2]: Verify no pre-loading occurs
  - When: App is freshly launched

### Error States
- **PREDEF-20**: Verify shelf handles invalid product data gracefully
  - Expected: The shelf is not rendered if products are invalid; No app crash occurs; Other modules on the page load normally

## API Dependencies

| Method | Endpoint | Description | Used In |
|--------|----------|-------------|---------|
| POST | `/api/v3/shopping-list/items` | Includes source field with platform-specific value | PREDEF-07, PREDEF-08, PREDEF-09 |

## Source Test Cases

- `Pre_Defined_Products/FRA-550_Pre_Defined_Product_Shelf.txt`
- Total: 20 test cases

<!-- MANUAL — Add your own notes below this line -->

## Manual Notes

<!-- Add accessibility IDs, navigation tips, tricky elements, etc. -->
