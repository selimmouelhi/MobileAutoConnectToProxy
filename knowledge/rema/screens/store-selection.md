# Store Selection Screen

<!-- AUTO-EXTRACTED -->
<!-- Extracted: 2026-04-01 14:24 -->

## Overview

Store picker and GPS-based store suggestions

## How to Reach

This screen is not directly accessible from the tab bar.

## Features on This Screen

- **[GPS Store Suggestions](../features/gps-store-suggestions.md)** — 7 test cases

## UI Elements

| Element | Mentions | Feature |
|---------|----------|---------|
| Hent checkout (screen) | 7 | GPS Store Suggestions |
| Vælg en anden butik | 4 | GPS Store Suggestions |
| Vælg butik | 3 | GPS Store Suggestions |
| GPS permission (dialog) | 3 | GPS Store Suggestions |
| Grant GPS permission if (prompt) | 2 | GPS Store Suggestions |
| Grant GPS permission when (prompt) | 1 | GPS Store Suggestions |
| Wait for GPS permission (dialog) | 1 | GPS Store Suggestions |

## APIs Used

- `GET /api/v3/stores/suggested` — Returns non-empty list of stores
- `GET /api/v3/stores?filter[near_coordinates]=<latitude>,<longitude>&filter[is_click_and_collect_active]=true&per_page=3` — Returns stores near user location

<!-- MANUAL — Add your own notes below this line -->

## Manual Notes

<!-- Add accessibility IDs, element XPaths from real Appium sessions, etc. -->
