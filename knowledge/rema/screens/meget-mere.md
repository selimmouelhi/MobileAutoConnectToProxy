# Meget mere Screen

<!-- AUTO-EXTRACTED -->
<!-- Extracted: 2026-04-01 14:24 -->

## Overview

More tab with profile, settings, help, etc.
- **Tab name**: Meget mere

## How to Reach

1. From any screen, tap the **Meget mere** tab in the bottom navigation bar

## Features on This Screen

- **[Vigo](../features/vigo.md)** — 25 test cases
- **[Zendesk Help](../features/zendesk-help.md)** — 49 test cases
- **[FAQ Help Page](../features/faq-help.md)** — 12 test cases
- **[Meget Mere](../features/meget-mere.md)** — 20 test cases

## UI Elements

| Element | Mentions | Feature |
|---------|----------|---------|
| Help (button) | 49 | Zendesk Help |
| and tap the help (button) | 48 | Zendesk Help |
| FAQ (button) | 10 | FAQ Help Page |
| Navigate to Settings (screen) | 8 | Vigo |
| menu (item) | 8 | Meget Mere |
| Tap the FAQ (button) | 7 | FAQ Help Page |
| Få dine varer leveret | 6 | Vigo |
| is visible on (menu) | 6 | Meget Mere |
| Settings (screen) | 4 | Meget Mere, Vigo |
| Navigate to Shopping List (screen) | 4 | Vigo |
| Vigo-indkøber | 4 | Vigo |
| Indstillinger | 4 | Meget Mere, Vigo |
| with FAQ (button) | 4 | FAQ Help Page |
| Server: Preprod | 4 | Meget Mere |
| Tap Login (button) | 3 | Vigo |
| Wait for home (screen) | 3 | Vigo |
| Navigate to Meget mere (screen) | 3 | Vigo |
| NO Vigo (menu) | 3 | Vigo |
| Observe the (button) | 3 | FAQ Help Page |
| Dine stjerner | 3 | Meget Mere |

## APIs Used

- `GET /api/v1/feature-flags` — Should NOT contain Vigo flags in response
- `POST /api/v1/auth/login` — Should NOT trigger Vigo flag fetches
- `POST /api/v1/account/switch` — Should NOT trigger Vigo flag fetches
- `GET /api/v1/shopping-list` — Returns current shopping list
- `POST /api/v1/shopping-list/items` — Adds items successfully
- `POST /api/v1/checkout` — Returns 200 with order confirmation

<!-- MANUAL — Add your own notes below this line -->

## Manual Notes

<!-- Add accessibility IDs, element XPaths from real Appium sessions, etc. -->
