# Favorite Recipes

<!-- AUTO-EXTRACTED — Do not edit above this line manually -->
<!-- Extracted: 2026-04-01 14:24 | Source: 28 test cases -->

## Overview

Feature area covering 28 test cases. Key areas:
- Verify updated search bar design on recipes screen
- Verify search bar clear icon and cancel behavior
- Verify favorites button appears next to search bar
- Verify favorites button transitions to Cancel when search is active
- Verify favorite icon displayed on recipe cards
- ... and 23 more

## Navigation

- **FAVREC-01**: User is on the Recipes screen
- **FAVREC-02**: User is on the Recipes screen → Tap on the search bar to activate it → Tap the clear icon
- **FAVREC-04**: User is on the Recipes screen → Tap on the search bar to activate it
- **FAVREC-05**: User is on the Recipes screen with recipe cards visible
- **FAVREC-06**: User is on the Recipes screen → Tap the heart/favorites icon on the recipe card
- **FAVREC-07**: User is on the Recipes screen → Tap the filled heart/favorites icon on the recipe card
- **FAVREC-08**: User is on the Recipes screen → Tap on a recipe card to open recipe details
- **FAVREC-09**: User has opened a recipe that is NOT yet favorited → Tap the favorite (heart) icon in the nav bar
- **FAVREC-10**: User has opened a recipe that IS already favorited → Tap the filled favorite (heart) icon in the nav bar

## UI Elements

| Element | Mentions | Referenced In |
|---------|----------|---------------|
| heart (icon) | 6 | FAVREC-06, FAVREC-07, FAVREC-09, FAVREC-10, FAVREC-25 +1 |
| Tap the favorites (button) | 5 | FAVREC-11, FAVREC-12, FAVREC-18, FAVREC-22, FAVREC-26 |
| Observe the (icon) | 4 | FAVREC-06, FAVREC-07, FAVREC-09, FAVREC-10 |
| next to the search (bar) | 4 | FAVREC-11, FAVREC-12, FAVREC-18, FAVREC-26 |
| The (icon) | 3 | FAVREC-03, FAVREC-05, FAVREC-28 |
| Tap the heart/favorites (icon) | 3 | FAVREC-06, FAVREC-16, FAVREC-19 |
| icon in the nav (bar) | 3 | FAVREC-09, FAVREC-10, FAVREC-28 |
| login (prompt) | 3 | FAVREC-16, FAVREC-17, FAVREC-18 |
| bottom (sheet) | 3 | FAVREC-16, FAVREC-17, FAVREC-18 |
| not the full login (screen) | 3 | FAVREC-16, FAVREC-17, FAVREC-18 |
| The (prompt) | 3 | FAVREC-16, FAVREC-17, FAVREC-18 |
| Dismissing the (prompt) | 3 | FAVREC-16, FAVREC-17, FAVREC-18 |
| Search (bar) | 2 | FAVREC-01, FAVREC-02 |
| Tap on the search (bar) | 2 | FAVREC-02, FAVREC-04 |
| heart/favorites (icon) | 2 | FAVREC-03, FAVREC-05 |
| Cancel | 2 | FAVREC-04 |
| Favorite recipes (screen) | 2 | FAVREC-11, FAVREC-12 |
| Tap the filled heart (icon) | 2 | FAVREC-13, FAVREC-24 |
| returns user to the Recipes (screen) | 2 | FAVREC-16, FAVREC-18 |
| Navigate to the Recipes (screen) | 2 | FAVREC-20, FAVREC-27 |
| Tapping the favorites (button) | 2 | FAVREC-20, FAVREC-27 |
| Tap the heart (icon) | 2 | FAVREC-21, FAVREC-23 |
| the heart (icon) | 2 | FAVREC-23, FAVREC-24 |
| Observe the search (bar) | 1 | FAVREC-01 |
| at the top of the Recipes (screen) | 1 | FAVREC-01 |

## Behaviors

### Normal Flow (P0/P1)
- **FAVREC-01** [P1]: Verify updated search bar design on recipes screen
  - Expected: Search bar uses updated background and border colors per Figma; New search icon is displayed and positioned slightly to the left compared to previous 
- **FAVREC-02** [P1]: Verify search bar clear icon and cancel behavior
  - Expected: New clear icon (X) is displayed inside the search bar when text is entered; Tapping the clear icon removes the entered text; Search bar remains active
- **FAVREC-03** [P0]: Verify favorites button appears next to search bar
  - Expected: A heart/favorites icon button is displayed to the right of the search bar; The icon matches the Figma design specifications
- **FAVREC-04** [P1]: Verify favorites button transitions to Cancel when search is active
  - Expected: The favorites button is replaced by a "Cancel" text button; Tapping "Cancel" deactivates the search bar and restores the favorites button
- **FAVREC-05** [P0]: Verify favorite icon displayed on recipe cards
  - Expected: A heart/favorites icon is displayed on each recipe card; The icon position and size match the Figma design; Unfavorited recipes show an empty/outline 
- **FAVREC-07** [P0]: Verify removing a recipe from favorites from recipe card
  - Expected: The heart icon transitions from filled to outline (empty) state; The change is immediate (optimistic UI update); The recipe is removed from the user's
- **FAVREC-08** [P1]: Verify recipe details nav bar shows updated icons
  - Expected: Dismiss (back/close) icon uses the new asset and matches Figma size and alignment; Share icon uses the new asset and matches Figma alignment; Favorite
- **FAVREC-10** [P0]: Verify removing a recipe from favorites from recipe details
  - Expected: The heart icon transitions from filled to outline state; The recipe is removed from the user's favorites list
- **FAVREC-11** [P0]: Verify navigating to favorite recipes list
  - Expected: Favorite recipes screen/view is displayed; All previously favorited recipes are shown; Each recipe card displays the filled heart icon
- **FAVREC-12** [P1]: Verify favorite recipes list is empty when no favorites exist
  - Expected: Favorite recipes screen/view is displayed; An empty state is shown (no recipes listed); Appropriate empty state message or illustration is displayed

### Edge Cases
- **FAVREC-06** [P0]: Verify adding a recipe to favorites from recipe card
  - When: User is logged in; User is on the Recipes screen; A recipe that is NOT yet favorited is visible
- **FAVREC-09** [P0]: Verify adding a recipe to favorites from recipe details
  - When: User is logged in; User has opened a recipe that is NOT yet favorited; Recipe details screen is displayed
- **FAVREC-16** [P0]: Verify login prompt when logged-out user taps favorite on recipe card
  - When: User is NOT logged in; User is on the Recipes screen with recipe cards visible
- **FAVREC-17** [P0]: Verify login prompt when logged-out user taps favorite on recipe details
  - When: User is NOT logged in; User is viewing a recipe details screen
- **FAVREC-18** [P0]: Verify login prompt when logged-out user taps favorites button next to search bar
  - When: User is NOT logged in; User is on the Recipes screen
- **FAVREC-19** [P1]: Verify successful login from favorite login prompt adds the recipe to favorites
  - When: User is NOT logged in; User is on the Recipes screen
- **FAVREC-25** [P2]: Verify rapid tap on favorite icon does not cause inconsistent state
  - When: User is logged in; User is on the Recipes screen
- **FAVREC-26** [P2]: Verify favorites list loads correctly with many favorited recipes
  - When: User is logged in; User has favorited a large number of recipes (20+)
- **FAVREC-27** [P2]: Verify favorite state is user-specific (not shared between accounts)
  - When: Two different user accounts exist (User A and User B); User A has favorited recipes; User B has not

### Error States
- **FAVREC-23**: Verify behavior when favorite API call fails (network error)
  - Expected: If optimistic UI was applied, the heart icon reverts to outline state; An error message or toast is displayed indicating the action failed; The recipe
- **FAVREC-24**: Verify behavior when unfavorite API call fails (network error)
  - Expected: If optimistic UI was applied, the heart icon reverts to filled state; An error message or toast is displayed indicating the action failed; The recipe 

## API Dependencies

| Method | Endpoint | Description | Used In |
|--------|----------|-------------|---------|
| GET | `/api/v3/users/{user-id}/favorite-recipes?fields=id` |  | FAVREC-03, FAVREC-05, FAVREC-20, FAVREC-21, FAVREC-22 +1 |
| POST | `/api/v3/users/{user-id}/favorite-recipes/{recipe_id}` |  | FAVREC-06, FAVREC-09, FAVREC-19, FAVREC-23, FAVREC-25 |
| DELETE | `/api/v3/users/{user-id}/favorite-recipes/{recipe-id}` |  | FAVREC-07, FAVREC-10, FAVREC-13, FAVREC-24, FAVREC-25 |
| GET | `/api/v3/users/{user-id}/favorite-recipes` |  | FAVREC-11, FAVREC-12, FAVREC-26 |

## Platform Notes

### iOS-Specific
- **FAVREC-28**: Verify dismiss icon size and alignment on recipe details (iOS-specific)

## Source Test Cases

- `Favorite_Recipes/FRA-549_favorite_recipes_test_cases.txt`
- Total: 28 test cases

<!-- MANUAL — Add your own notes below this line -->

## Manual Notes

<!-- Add accessibility IDs, navigation tips, tricky elements, etc. -->
