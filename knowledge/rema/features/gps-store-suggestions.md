# GPS Store Suggestions

<!-- AUTO-EXTRACTED — Do not edit above this line manually -->
<!-- Extracted: 2026-04-01 14:24 | Source: 7 test cases -->

## Overview

Feature area covering 7 test cases. Key areas:
- Default suggested stores displayed without GPS fallback
- GPS fallback triggered when default suggestions are empty
- GPS permission denied by user
- GPS timeout handling after 3 seconds
- GPS disabled on device
- ... and 2 more

## Navigation

- **FRA-01**: Navigate to Køb & Hent checkout screen

## UI Elements

| Element | Mentions | Referenced In |
|---------|----------|---------------|
| Hent checkout (screen) | 7 | FRA-01, FRA-02, FRA-03, FRA-04, FRA-05 +2 |
| Vælg en anden butik | 4 | FRA-03, FRA-04, FRA-05, FRA-06 |
| Vælg butik | 3 | FRA-01, FRA-02, FRA-07 |
| GPS permission (dialog) | 3 | FRA-02, FRA-03, FRA-07 |
| Grant GPS permission if (prompt) | 2 | FRA-04, FRA-06 |
| Grant GPS permission when (prompt) | 1 | FRA-02 |
| Wait for GPS permission (dialog) | 1 | FRA-03 |

## Behaviors

### Edge Cases
- **FRA-01**: Default suggested stores displayed without GPS fallback
  - When: User is logged in with a registered delivery address; GPS permission not yet requested
- **FRA-02**: GPS fallback triggered when default suggestions are empty
  - When: User is logged in; Default suggested stores endpoint returns empty list; GPS permission not yet granted
- **FRA-03**: GPS permission denied by user
  - When: User is logged in; Default suggested stores endpoint returns empty list; GPS permission not yet granted
- **FRA-04**: GPS timeout handling after 3 seconds
  - When: User is logged in; Default suggested stores endpoint returns empty list; GPS permission is granted
- **FRA-05**: GPS disabled on device
  - When: User is logged in; Default suggested stores endpoint returns empty list; GPS permission is granted but GPS is disabled in device settings
- **FRA-06**: No stores found even with GPS coordinates
  - When: User is logged in in a remote area with no nearby stores; Default suggested stores endpoint returns empty list; GPS permission is granted and location
- **FRA-07**: GPS permission already granted from previous session
  - When: User is logged in; GPS permission was granted in a previous session; Default suggested stores endpoint returns empty list

## API Dependencies

| Method | Endpoint | Description | Used In |
|--------|----------|-------------|---------|
| GET | `/api/v3/stores/suggested` | Returns non-empty list of stores | FRA-01, FRA-02, FRA-03, FRA-04, FRA-05 +2 |
| GET | `/api/v3/stores?filter[near_coordinates]=<latitude>,<longitude>&filter[is_click_and_collect_active]=true&per_page=3` | Returns stores near user location | FRA-02, FRA-06, FRA-07 |

## Source Test Cases

- `GPS_Store_Suggestions/FRA-572_GPS_Store_Suggestions.txt`
- Total: 7 test cases

<!-- MANUAL — Add your own notes below this line -->

## Manual Notes

<!-- Add accessibility IDs, navigation tips, tricky elements, etc. -->
