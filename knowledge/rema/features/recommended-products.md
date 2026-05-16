# Recommended Products

<!-- AUTO-EXTRACTED — Do not edit above this line manually -->
<!-- Extracted: 2026-04-01 14:24 | Source: 49 test cases -->

## Overview

Feature area covering 49 test cases. Key areas:
- Recommendations shelf displayed with all prerequisites met
- Shelf hidden when personalization policy not accepted
- Shelf hidden when user is not logged in
- Shelf hidden when no shopping list is selected
- Shelf hidden when selected shopping list is empty
- ... and 44 more

## Navigation

- **RecommendedList 01**: App has been launched and pre-loading completed → Navigate to pre-search screen
- **RecommendedList 02**: Navigate to pre-search screen
- **RecommendedList 08**: Tap "See all" button on recommendations shelf
- **RecommendedList 11**: Navigate to pre-search screen or trigger refresh

## UI Elements

| Element | Mentions | Referenced In |
|---------|----------|---------------|
| Navigate to pre-search (screen) | 15 | RecommendedList 01, RecommendedList 02, RecommendedList 03, RecommendedList 04, RecommendedList 05 +10 |
| Add (item) | 13 | RecommendedList 44 |
| Recommended products from active list | 8 | RecommendedList 01, RecommendedList 02, RecommendedList 03, RecommendedList 04, RecommendedList 05 +3 |
| Observe recommendations (shelf) | 7 | RecommendedList 13, RecommendedList 15, RecommendedList 18, RecommendedList 19, RecommendedList 21 +2 |
| Recommendations (shelf) | 6 | RecommendedList 14, RecommendedList 16, RecommendedList 27, RecommendedList 28, RecommendedList 34 +1 |
| Navigate back to pre-search (screen) | 4 | RecommendedList 12, RecommendedList 17, RecommendedList 27, RecommendedList 28 |
| See all | 2 | RecommendedList 01, RecommendedList 08 |
| Skeleton loader is displayed on recommendations (shelf) | 2 | RecommendedList 15, RecommendedList 17 |
| android_recommendations_from_active_list | 2 | RecommendedList 23, RecommendedList 24 |
| ios_recommendations_from_active_list | 2 | RecommendedList 23, RecommendedList 24 |
| Wait for recommendations (shelf) | 1 | RecommendedList 01 |
| Products (carousel) | 1 | RecommendedList 01 |
| Shelf uses same design as popular products (carousel) | 1 | RecommendedList 01 |
| Products are based on (item) | 1 | RecommendedList 01 |
| Enter any search query in search (field) | 1 | RecommendedList 07 |
| Shelf reappears when search (field) | 1 | RecommendedList 07 |
| button on recommendations (shelf) | 1 | RecommendedList 08 |
| Same loading state as other product (shelf) | 1 | RecommendedList 08 |
| Each product shows add to list (button) | 1 | RecommendedList 08 |
| Error state is displayed for recommendations (shelf) | 1 | RecommendedList 09 |
| Same error UI as used for popular products (shelf) | 1 | RecommendedList 09 |
| Popular products | 1 | RecommendedList 15 |
| Navigate to shopping list (view) | 1 | RecommendedList 17 |
| Remove a product from shopping list via recommendations (shelf) | 1 | RecommendedList 21 |
| add (button) | 1 | RecommendedList 21 |

## Behaviors

### Edge Cases
- **RecommendedList 01**: Recommendations shelf displayed with all prerequisites met
  - When: User is logged in; Personalization policy is accepted; Shopping list is selected and contains products
- **RecommendedList 02**: Shelf hidden when personalization policy not accepted
  - When: User is logged in; Personalization policy is NOT accepted; Shopping list is selected and contains products
- **RecommendedList 03**: Shelf hidden when user is not logged in
  - When: User is NOT logged in (guest user)
- **RecommendedList 04**: Shelf hidden when no shopping list is selected
  - When: User is logged in; Personalization policy is accepted; No shopping list is currently selected
- **RecommendedList 05**: Shelf hidden when selected shopping list is empty
  - When: User is logged in; Personalization policy is accepted; Shopping list is selected but contains zero products
- **RecommendedList 06**: Shelf hidden when API returns empty product list
  - When: User is logged in; Personalization policy is accepted; Shopping list is selected and contains products
- **RecommendedList 07**: Shelf only displayed in pre-search, not in search results
  - When: User is logged in; Personalization policy is accepted; Shopping list is selected and contains products
- **RecommendedList 08**: See all button opens product list page
  - When: User is logged in; Shopping list is selected and contains products; Recommendations shelf is displayed
- **RecommendedList 10**: Skeleton loader displayed while loading
  - When: User is logged in; Personalization policy is accepted; Shopping list is selected and contains products
- **RecommendedList 11**: Products reload after 1 hour cache invalidation
  - When: User is logged in; Personalization policy is accepted; Shopping list is selected and contains products

### Error States
- **RecommendedList 09**: Error state displayed when API call fails
  - Expected: Error state is displayed for recommendations shelf; Same error UI as used for popular products shelf; User can retry by pulling to refresh
- **RecommendedList 31**: Network connectivity lost and restored
  - Expected: During offline: Cached recommendations remain visible; After reconnection: Skeleton loader displays; API call is made to fetch updated recommendations

## API Dependencies

| Method | Endpoint | Description | Used In |
|--------|----------|-------------|---------|
| GET | `/api/recommendations/active-list` | Returns list of recommended products | RecommendedList 01, RecommendedList 06, RecommendedList 09, RecommendedList 10, RecommendedList 11 +19 |
| POST | `/api/shopping-list/items` | Request includes platform-specific source | RecommendedList 23, RecommendedList 24 |
| GET | `/api/products/{product_id}` | Fetches product details | RecommendedList 25, RecommendedList 26 |
| GET | `/api/contentful` | Returns shelf configuration | RecommendedList 36 |

## Source Test Cases

- `Recommended_Products/FRA-555_Recommended_Products_Active_List.txt`
- Total: 49 test cases

<!-- MANUAL — Add your own notes below this line -->

## Manual Notes

<!-- Add accessibility IDs, navigation tips, tricky elements, etc. -->
