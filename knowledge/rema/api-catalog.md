# Rema App — API Catalog

<!-- AUTO-EXTRACTED -->
<!-- Extracted: 2026-04-01 14:24 -->

All API endpoints discovered from test case documentation.

## Favorite Recipes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/users/{user-id}/favorite-recipes?fields=id` |  |
| POST | `/api/v3/users/{user-id}/favorite-recipes/{recipe_id}` |  |
| DELETE | `/api/v3/users/{user-id}/favorite-recipes/{recipe-id}` |  |
| GET | `/api/v3/users/{user-id}/favorite-recipes` |  |

## GPS Store Suggestions

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v3/stores/suggested` | Returns non-empty list of stores |
| GET | `/api/v3/stores?filter[near_coordinates]=<latitude>,<longitude>&filter[is_click_and_collect_active]=true&per_page=3` | Returns stores near user location |

## Payment Methods

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/feature-flags` | Returns mobilePay and worldline flags as true |

## Pre-Defined Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v3/shopping-list/items` | Includes source field with platform-specific value |

## Recommended Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/recommendations/active-list` | Returns list of recommended products |
| POST | `/api/shopping-list/items` | Request includes platform-specific source |
| GET | `/api/products/{product_id}` | Fetches product details |
| GET | `/api/contentful` | Returns shelf configuration |

## Share Shopping List

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v3/invitation-links/{id}` | Legacy auto-accept flow |
| GET | `/api/v1/shoppinglists/polling` | Syncs shared list data |
| GET | `/api/v3/users/{id}/shopping-list-invitations` | Shows pending invitation before auto-accept |
| DELETE | `/api/v1/shoppinglists/{id}` | User B removes access |
| DELETE | `/api/v3/shopping-lists/{id}/members/{userId}` | Revoke access |
| GET | `/api/shopping-lists/{id}` | Returns shopping list with shared users data |

## Vigo

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/feature-flags` | Should NOT contain Vigo flags in response |
| POST | `/api/v1/auth/login` | Should NOT trigger Vigo flag fetches |
| POST | `/api/v1/account/switch` | Should NOT trigger Vigo flag fetches |
| GET | `/api/v1/shopping-list` | Returns current shopping list |
| POST | `/api/v1/shopping-list/items` | Adds items successfully |
| POST | `/api/v1/checkout` | Returns 200 with order confirmation |

## All Endpoints (Deduplicated)

| Method | Endpoint | Features |
|--------|----------|----------|
| DELETE | `/api/v1/shoppinglists/{id}` | Share Shopping List |
| DELETE | `/api/v3/shopping-lists/{id}/members/{userId}` | Share Shopping List |
| DELETE | `/api/v3/users/{user-id}/favorite-recipes/{recipe-id}` | Favorite Recipes |
| GET | `/api/contentful` | Recommended Products |
| GET | `/api/feature-flags` | Payment Methods |
| GET | `/api/products/{product_id}` | Recommended Products |
| GET | `/api/recommendations/active-list` | Recommended Products |
| GET | `/api/shopping-lists/{id}` | Share Shopping List |
| GET | `/api/v1/feature-flags` | Vigo |
| GET | `/api/v1/shopping-list` | Vigo |
| GET | `/api/v1/shoppinglists/polling` | Share Shopping List |
| GET | `/api/v3/stores/suggested` | GPS Store Suggestions |
| GET | `/api/v3/stores?filter[near_coordinates]=<latitude>,<longitude>&filter[is_click_and_collect_active]=true&per_page=3` | GPS Store Suggestions |
| GET | `/api/v3/users/{id}/shopping-list-invitations` | Share Shopping List |
| GET | `/api/v3/users/{user-id}/favorite-recipes` | Favorite Recipes |
| GET | `/api/v3/users/{user-id}/favorite-recipes?fields=id` | Favorite Recipes |
| POST | `/api/shopping-list/items` | Recommended Products |
| POST | `/api/v1/account/switch` | Vigo |
| POST | `/api/v1/auth/login` | Vigo |
| POST | `/api/v1/checkout` | Vigo |
| POST | `/api/v1/shopping-list/items` | Vigo |
| POST | `/api/v3/invitation-links/{id}` | Share Shopping List |
| POST | `/api/v3/shopping-list/items` | Pre-Defined Products |
| POST | `/api/v3/users/{user-id}/favorite-recipes/{recipe_id}` | Favorite Recipes |

## Known Feature Flags

| Flag | Feature |
|------|---------|
| `app.android.payments.mobilePay` | Payment Methods |
| `app.android.payments.worldline` | Payment Methods |
| `app.ios.payments.mobilePay` | Payment Methods |
| `app.android.vigo` | Vigo |
| `app.ios.vigo` | Vigo |

<!-- MANUAL -->

## Manual Notes

<!-- Add base URL, auth requirements, environment-specific endpoints, etc. -->
