# Vigo

<!-- AUTO-EXTRACTED — Do not edit above this line manually -->
<!-- Extracted: 2026-04-01 14:24 | Source: 25 test cases -->

## Overview

Feature area covering 25 test cases. Key areas:
- Verify feature flag cache expiration and refresh
- Verify fallback to Vigo enabled when feature flag parsing fails
- Verify rating stars section is removed from settings
- Verify Vigo menu item is removed from Meget mere screen
- Verify "Få dine varer leveret" button is removed from shopping list
- ... and 20 more

## Navigation

- **VIGO-38**: Open app after 24+ hour period
- **VIGO-39**: User launches app → Launch app → Navigate to rating stars section → Navigate to Vigo menu
- **VIGO-01**: Navigate to Settings screen
- **VIGO-02**: Navigate to Meget mere (More) screen
- **VIGO-03**: Navigate to Shopping List screen
- **VIGO-05**: Navigate to Vigo screen
- **VIGO-07**: Launch the app → Monitor network traffic during launch
- **VIGO-08**: Tap Login button

## UI Elements

| Element | Mentions | Referenced In |
|---------|----------|---------------|
| Navigate to Settings (screen) | 8 | VIGO-01, VIGO-04, VIGO-06, VIGO-12, VIGO-13 +3 |
| Få dine varer leveret | 6 | VIGO-03, VIGO-12, VIGO-13, VIGO-14, VIGO-18 |
| Navigate to Shopping List (screen) | 4 | VIGO-03, VIGO-12, VIGO-13, VIGO-14 |
| Vigo-indkøber | 4 | VIGO-04, VIGO-05, VIGO-20, VIGO-21 |
| Settings (screen) | 3 | VIGO-01, VIGO-20, VIGO-21 |
| Tap Login (button) | 3 | VIGO-08, VIGO-15, VIGO-16 |
| Wait for home (screen) | 3 | VIGO-08, VIGO-15, VIGO-16 |
| Navigate to Meget mere (screen) | 3 | VIGO-12, VIGO-13, VIGO-14 |
| NO Vigo (menu) | 3 | VIGO-12, VIGO-13, VIGO-14 |
| Home (screen) | 2 | VIGO-15, VIGO-16 |
| Verify no Vigo-related settings or (tab) | 2 | VIGO-20, VIGO-21 |
| Navigate to Vigo (menu) | 1 | VIGO-39 |
| No crashes or error (dialog) | 1 | VIGO-39 |
| Scroll through entire (menu) | 1 | VIGO-02 |
| Check for any Vigo-related (menu) | 1 | VIGO-02 |
| No Vigo (menu) | 1 | VIGO-02 |
| Meget mere (screen) | 1 | VIGO-02 |
| renders correctly with other (menu) | 1 | VIGO-02 |
| No empty spaces or layout issues where Vigo (menu) | 1 | VIGO-02 |
| Scroll through the entire shopping list (view) | 1 | VIGO-03 |
| Search for (button) | 1 | VIGO-03 |
| Check bottom action (button) | 1 | VIGO-03 |
| All other shopping list (button) | 1 | VIGO-03 |
| Check all available (tab) | 1 | VIGO-04 |
| Swipe horizontally to (view) | 1 | VIGO-04 |

## Behaviors

### Edge Cases
- **VIGO-38**: Verify feature flag cache expiration and refresh
  - When: User has app installed; Feature flags were fetched more than 24 hours ago; App has been running in background
- **VIGO-02**: Verify Vigo menu item is removed from Meget mere screen
  - When: User is logged in as a Customer; App is updated to version 6.3.0
- **VIGO-03**: Verify "Få dine varer leveret" button is removed from shopping list
  - When: User is logged in as a Customer; Shopping list contains items
- **VIGO-05**: Verify Vigo settings moved to Vigo screen for Scan Selv users
  - When: User is logged in with Scan Selv account; App is updated to version 6.3.0
- **VIGO-06**: Verify Settings title changed to "Indstillinger" on Android
  - When: App is running on Android device; User is logged in
- **VIGO-07**: Verify no Vigo feature flags on app launch
  - When: App is freshly installed or cleared from memory; Network monitoring tool is active
- **VIGO-08**: Verify no Vigo feature flags on login
  - When: User is logged out; Network monitoring tool is active
- **VIGO-09**: Verify no Vigo feature flags on account switch
  - When: User is logged in with first account; Second account is available for switching; Network monitoring tool is active
- **VIGO-10**: Verify no Vigo feature flags on app resume
  - When: App is running in background; Network monitoring tool is active
- **VIGO-11**: Verify backend does not send removed flags in response
  - When: App is connected to preprod environment; Network traffic monitoring is active

### Error States
- **VIGO-39**: Verify fallback to Vigo enabled when feature flag parsing fails
  - Expected: App safely handles unexpected flag structure; Falls back to default (Vigo enabled = true); All Vigo features are accessible
- **VIGO-01**: Verify rating stars section is removed from settings
  - Expected: Rating stars section is NOT displayed anywhere in settings; No UI elements related to rating functionality are present; Settings screen displays norma
- **VIGO-04**: Verify Vigo-indkøber tab is removed from settings
  - Expected: "Vigo-indkøber" tab is NOT displayed; Settings tabs display correctly without the removed tab; No navigation errors or crashes occur
- **VIGO-14**: Verify Vigo options not shown when flags are missing
  - Expected: NO Vigo menu items appear; NO rating stars section appears; NO "Få dine varer leveret" button appears
- **VIGO-15**: Verify login flow works correctly - Android
  - Expected: Login completes successfully without errors; Home screen loads correctly; No crashes or performance issues
- **VIGO-16**: Verify login flow works correctly - iOS
  - Expected: Login completes successfully without errors; Home screen loads correctly; No crashes or performance issues
- **VIGO-17**: Verify account switching works correctly
  - Expected: Account switch completes without errors; Store account loads correctly; No feature flag errors in logs
- **VIGO-18**: Verify shopping list functionality
  - Expected: Shopping list displays correctly; Add, remove, and mark operations work without errors; No "Få dine varer leveret" button is present
- **VIGO-19**: Verify checkout flow works correctly
  - Expected: Checkout flow completes successfully; No Vigo-related errors or UI glitches; Order confirmation is displayed
- **VIGO-23**: Verify app stability with multiple operations
  - Expected: App remains stable throughout all operations; No crashes or fatal errors occur; No feature flag errors appear in logs

## API Dependencies

| Method | Endpoint | Description | Used In |
|--------|----------|-------------|---------|
| GET | `/api/v1/feature-flags` | Should NOT contain Vigo flags in response | VIGO-07, VIGO-11, VIGO-12, VIGO-13, VIGO-14 |
| POST | `/api/v1/auth/login` | Should NOT trigger Vigo flag fetches | VIGO-08, VIGO-15, VIGO-16 |
| POST | `/api/v1/account/switch` | Should NOT trigger Vigo flag fetches | VIGO-09, VIGO-17 |
| GET | `/api/v1/shopping-list` | Returns current shopping list | VIGO-18 |
| POST | `/api/v1/shopping-list/items` | Adds items successfully | VIGO-18 |
| POST | `/api/v1/checkout` | Returns 200 with order confirmation | VIGO-19 |

## Feature Flags

- `app.android.vigo` — referenced in VIGO-07, VIGO-11
- `app.ios.vigo` — referenced in VIGO-07, VIGO-11

## Platform Notes

### iOS-Specific
- **VIGO-16**: Verify login flow works correctly - iOS

### Android-Specific
- **VIGO-06**: Verify Settings title changed to "Indstillinger" on Android
- **VIGO-15**: Verify login flow works correctly - Android

## Source Test Cases

- `Vigo/Shutdown_Release_1/vigo_shutdown_release_1_testcases.txt`
- `Vigo/Feature_Flag_Cleanup/vigo-feature-flag-cleanup-testcases-updated.txt`
- Total: 25 test cases

<!-- MANUAL — Add your own notes below this line -->

## Manual Notes

<!-- Add accessibility IDs, navigation tips, tricky elements, etc. -->
