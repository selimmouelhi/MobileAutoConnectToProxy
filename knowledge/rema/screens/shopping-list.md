# Shopping List Screen

<!-- AUTO-EXTRACTED -->
<!-- Extracted: 2026-04-01 14:24 -->

## Overview

Shopping list management, item adding, sharing, and ordering
- **Tab name**: Indkøbsliste

## How to Reach

1. From any screen, tap the **Indkøbsliste** tab in the bottom navigation bar

## Features on This Screen

- **[Share Shopping List](../features/share-shopping-list.md)** — 209 test cases
- **[Recommended Products](../features/recommended-products.md)** — 49 test cases
- **[Vigo](../features/vigo.md)** — 25 test cases
- **[Pre-Defined Products](../features/pre-defined-products.md)** — 20 test cases
- **[Shopping List Interactions](../features/regression-shopping-list.md)** — 13 test cases

## UI Elements

| Element | Mentions | Feature |
|---------|----------|---------|
| Who has access | 32 | Share Shopping List |
| Add (item) | 29 | Recommended Products, Shopping List Interactions, Vigo |
| Observe the (sheet) | 26 | Share Shopping List |
| invitation (sheet) | 26 | Share Shopping List |
| Observe the (screen) | 21 | Pre-Defined Products, Share Shopping List |
| Del liste | 18 | Share Shopping List |
| share shopping list (sheet) | 16 | Share Shopping List |
| The (button) | 15 | Share Shopping List |
| Navigate to pre-search (screen) | 15 | Recommended Products |
| Observe the (button) | 12 | Share Shopping List |
| Observe the share area on the shopping list (screen) | 10 | Share Shopping List |
| Tap the share list (button) | 10 | Share Shopping List |
| The (sheet) | 10 | Share Shopping List |
| Observe the invitation (sheet) | 9 | Share Shopping List |
| Luk | 8 | Share Shopping List |
| confirmation (sheet) | 8 | Share Shopping List |
| Tap the Share (link) | 8 | Share Shopping List |
| Recommended products from active list | 8 | Recommended Products |
| Navigate to Settings (screen) | 8 | Vigo |
| Navigate to the shopping list (screen) | 7 | Share Shopping List |

## APIs Used

- `POST /api/v3/invitation-links/{id}` — Legacy auto-accept flow
- `GET /api/v1/shoppinglists/polling` — Syncs shared list data
- `GET /api/v3/users/{id}/shopping-list-invitations` — Shows pending invitation before auto-accept
- `DELETE /api/v1/shoppinglists/{id}` — User B removes access
- `DELETE /api/v3/shopping-lists/{id}/members/{userId}` — Revoke access
- `GET /api/shopping-lists/{id}` — Returns shopping list with shared users data
- `GET /api/recommendations/active-list` — Returns list of recommended products
- `POST /api/shopping-list/items` — Request includes platform-specific source
- `GET /api/products/{product_id}` — Fetches product details
- `GET /api/contentful` — Returns shelf configuration
- `GET /api/v1/feature-flags` — Should NOT contain Vigo flags in response
- `POST /api/v1/auth/login` — Should NOT trigger Vigo flag fetches
- `POST /api/v1/account/switch` — Should NOT trigger Vigo flag fetches
- `GET /api/v1/shopping-list` — Returns current shopping list
- `POST /api/v1/shopping-list/items` — Adds items successfully
- `POST /api/v1/checkout` — Returns 200 with order confirmation
- `POST /api/v3/shopping-list/items` — Includes source field with platform-specific value

<!-- MANUAL — Add your own notes below this line -->

## Manual Notes

<!-- Add accessibility IDs, element XPaths from real Appium sessions, etc. -->
