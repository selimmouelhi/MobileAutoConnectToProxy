# Checkout Screen

<!-- AUTO-EXTRACTED -->
<!-- Extracted: 2026-04-01 14:24 -->

## Overview

Checkout flow: store selection, payment, order tracking

## How to Reach

This screen is not directly accessible from the tab bar.

## Features on This Screen

- **[Payment Methods](../features/payment-methods.md)** — 10 test cases
- **[GPS Store Suggestions](../features/gps-store-suggestions.md)** — 7 test cases
- **[Faster Picker Flow](../features/faster-picker-flow.md)** — 20 test cases
- **[Order Flow](../features/regression-order-flow.md)** — 3 test cases
- **[Job Picking](../features/regression-job-picking.md)** — 2 test cases

## UI Elements

| Element | Mentions | Feature |
|---------|----------|---------|
| Navigate to the job details (screen) | 20 | Faster Picker Flow |
| Amount picker (sheet) | 18 | Faster Picker Flow |
| Tap the payment method (selector) | 11 | Payment Methods |
| Observe the payment method bottom (sheet) | 9 | Payment Methods |
| Payment method bottom (sheet) | 9 | Payment Methods |
| Locate an (item) | 9 | Faster Picker Flow |
| Navigate to checkout (screen) | 8 | Payment Methods |
| Activate the (bar) | 8 | Faster Picker Flow |
| Hent checkout (screen) | 7 | GPS Store Suggestions |
| Scan the (bar) | 7 | Faster Picker Flow |
| Swipe the (item) | 5 | Faster Picker Flow |
| code of an (item) | 5 | Faster Picker Flow |
| Vælg en anden butik | 4 | GPS Store Suggestions |
| Loading indicator appears in the job (item) | 4 | Faster Picker Flow |
| Both MobilePay and Worldline (button) | 3 | Payment Methods |
| Vælg butik | 3 | GPS Store Suggestions |
| GPS permission (dialog) | 3 | GPS Store Suggestions |
| Total area updates to reflect the picked (item) | 3 | Faster Picker Flow |
| MobilePay (button) | 2 | Payment Methods |
| Worldline (button) | 2 | Payment Methods |

## APIs Used

- `GET /api/feature-flags` — Returns mobilePay and worldline flags as true
- `GET /api/v3/stores/suggested` — Returns non-empty list of stores
- `GET /api/v3/stores?filter[near_coordinates]=<latitude>,<longitude>&filter[is_click_and_collect_active]=true&per_page=3` — Returns stores near user location

<!-- MANUAL — Add your own notes below this line -->

## Manual Notes

<!-- Add accessibility IDs, element XPaths from real Appium sessions, etc. -->
