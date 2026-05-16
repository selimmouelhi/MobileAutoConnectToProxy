# Meget Mere

<!-- AUTO-EXTRACTED — Do not edit above this line manually -->
<!-- Extracted: 2026-04-01 14:24 | Source: 20 test cases -->

## Overview

Feature area covering 20 test cases. Key areas:
- Verify Meget Mere screen displays all primary elements
- Verify user profile section displays correctly
- Verify star rating display functionality
- Navigate to Indstillinger (Settings) screen
- Verify Server environment indicator displays
- ... and 15 more

## Navigation

- **MEGETMERE-01**: User has navigated to the Meget Mere (More) tab
- **MEGETMERE-02**: User is on the Meget Mere screen
- **MEGETMERE-04**: User is on the Meget Mere screen → Tap "Indstillinger" button
- **MEGETMERE-06**: User is on the Meget Mere screen → Tap "Vigo" menu item
- **MEGETMERE-07**: User is on the Meget Mere screen → Tap "Dine indkøbsopgaver" menu item
- **MEGETMERE-08**: User is on the Meget Mere screen → Tap "Butikker og åbningstider" menu item
- **MEGETMERE-09**: User is on the Meget Mere screen → Tap "Aviser" menu item
- **MEGETMERE-10**: User is on the Meget Mere screen → Tap "Varescanner" menu item

## UI Elements

| Element | Mentions | Referenced In |
|---------|----------|---------------|
| menu (item) | 8 | MEGETMERE-06, MEGETMERE-07, MEGETMERE-08, MEGETMERE-09, MEGETMERE-10 +1 |
| is visible on (menu) | 6 | MEGETMERE-06, MEGETMERE-07, MEGETMERE-08, MEGETMERE-09, MEGETMERE-10 +1 |
| Server: Preprod | 4 | MEGETMERE-01, MEGETMERE-05, MEGETMERE-13 |
| Dine stjerner | 3 | MEGETMERE-01, MEGETMERE-03, MEGETMERE-19 |
| Indstillinger | 3 | MEGETMERE-01, MEGETMERE-04, MEGETMERE-13 |
| Kontakt kundeservice | 3 | MEGETMERE-12, MEGETMERE-14 |
| Vilkår & samtykke | 3 | MEGETMERE-12, MEGETMERE-15 |
| Bottom navigation (bar) | 2 | MEGETMERE-01, MEGETMERE-16 |
| Varescanner | 2 | MEGETMERE-10 |
| Nyhedsbreve | 2 | MEGETMERE-11 |
| Meget mere (tab) | 2 | MEGETMERE-16, MEGETMERE-17 |
| Observe the (screen) | 1 | MEGETMERE-01 |
| Profile section displays at top with user (icon) | 1 | MEGETMERE-01 |
| button appears with gear (icon) | 1 | MEGETMERE-01 |
| button appears with server (icon) | 1 | MEGETMERE-01 |
| Menu card displays with all (item) | 1 | MEGETMERE-01 |
| Each (menu) | 1 | MEGETMERE-01 |
| item shows appropriate (icon) | 1 | MEGETMERE-01 |
| is visible with Meget mere (tab) | 1 | MEGETMERE-01 |
| Observe the profile section at top of (screen) | 1 | MEGETMERE-02 |
| User (icon) | 1 | MEGETMERE-02 |
| Profile section is positioned at the top of the (screen) | 1 | MEGETMERE-02 |
| App navigates to the Settings (screen) | 1 | MEGETMERE-04 |
| Settings (screen) | 1 | MEGETMERE-04 |
| Back navigation is available to return to Meget Mere (screen) | 1 | MEGETMERE-04 |

## Behaviors

### Edge Cases
- **MEGETMERE-01**: Verify Meget Mere screen displays all primary elements
  - When: User is logged in to the Rema mobile app; User has navigated to the Meget Mere (More) tab
- **MEGETMERE-02**: Verify user profile section displays correctly
  - When: User is logged in to the Rema mobile app; User is on the Meget Mere screen
- **MEGETMERE-03**: Verify star rating display functionality
  - When: User is logged in with an active loyalty account; User is on the Meget Mere screen
- **MEGETMERE-04**: Navigate to Indstillinger (Settings) screen
  - When: User is logged in to the Rema mobile app; User is on the Meget Mere screen
- **MEGETMERE-05**: Verify Server environment indicator displays
  - When: User is on the Meget Mere screen; App is connected to Preprod environment
- **MEGETMERE-06**: Navigate to Vigo screen
  - When: User is logged in to the Rema mobile app; User is on the Meget Mere screen
- **MEGETMERE-07**: Navigate to Dine indkøbsopgaver (Shopping Tasks)
  - When: User is logged in to the Rema mobile app; User is on the Meget Mere screen
- **MEGETMERE-08**: Navigate to Butikker og åbningstider (Stores and Hours)
  - When: User is logged in to the Rema mobile app; User is on the Meget Mere screen
- **MEGETMERE-09**: Navigate to Aviser (Flyers) screen
  - When: User is logged in to the Rema mobile app; User is on the Meget Mere screen
- **MEGETMERE-10**: Navigate to Varescanner (Product Scanner)
  - When: User is logged in to the Rema mobile app; User is on the Meget Mere screen

### Error States
- **MEGETMERE-20**: Verify offline behavior on Meget Mere screen
  - Expected: Cached content remains visible if previously loaded; Error message displays if data cannot be refreshed; Offline indicator may appear

## API Dependencies

No API endpoints documented in test cases.

## Source Test Cases

- `Meget_Mere/testcases_megetmere_screen.txt`
- Total: 20 test cases

<!-- MANUAL — Add your own notes below this line -->

## Manual Notes

<!-- Add accessibility IDs, navigation tips, tricky elements, etc. -->
