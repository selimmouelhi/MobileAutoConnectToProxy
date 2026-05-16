# Recipes Screen

<!-- AUTO-EXTRACTED -->
<!-- Extracted: 2026-04-01 14:24 -->

## Overview

Recipe browsing, search, favorites, and cooking flow
- **Tab name**: Opskrifter

## How to Reach

1. From any screen, tap the **Opskrifter** tab in the bottom navigation bar

## Features on This Screen

- **[Favorite Recipes](../features/favorite-recipes.md)** — 28 test cases
- **[Recipe Flow](../features/regression-recipe-flow.md)** — 2 test cases

## UI Elements

| Element | Mentions | Feature |
|---------|----------|---------|
| heart (icon) | 6 | Favorite Recipes |
| Tap the favorites (button) | 5 | Favorite Recipes |
| Observe the (icon) | 4 | Favorite Recipes |
| next to the search (bar) | 4 | Favorite Recipes |
| The (icon) | 3 | Favorite Recipes |
| Tap the heart/favorites (icon) | 3 | Favorite Recipes |
| icon in the nav (bar) | 3 | Favorite Recipes |
| login (prompt) | 3 | Favorite Recipes |
| bottom (sheet) | 3 | Favorite Recipes |
| not the full login (screen) | 3 | Favorite Recipes |
| The (prompt) | 3 | Favorite Recipes |
| Dismissing the (prompt) | 3 | Favorite Recipes |
| Search (bar) | 2 | Favorite Recipes |
| Tap on the search (bar) | 2 | Favorite Recipes |
| heart/favorites (icon) | 2 | Favorite Recipes |
| Cancel | 2 | Favorite Recipes |
| Favorite recipes (screen) | 2 | Favorite Recipes |
| Tap the filled heart (icon) | 2 | Favorite Recipes |
| returns user to the Recipes (screen) | 2 | Favorite Recipes |
| Navigate to the Recipes (screen) | 2 | Favorite Recipes |

## APIs Used

- `GET /api/v3/users/{user-id}/favorite-recipes?fields=id` — 
- `POST /api/v3/users/{user-id}/favorite-recipes/{recipe_id}` — 
- `DELETE /api/v3/users/{user-id}/favorite-recipes/{recipe-id}` — 
- `GET /api/v3/users/{user-id}/favorite-recipes` — 

<!-- MANUAL — Add your own notes below this line -->

## Manual Notes

<!-- Add accessibility IDs, element XPaths from real Appium sessions, etc. -->
