# Faster Picker Flow

<!-- AUTO-EXTRACTED — Do not edit above this line manually -->
<!-- Extracted: 2026-04-01 14:24 | Source: 20 test cases -->

## Overview

Feature area covering 20 test cases. Key areas:
- Swipe to pick item with quantity 1 - Success flow
- Swipe to pick item with quantity 1 - API failure
- Swipe to pick item with quantity greater than 1 - Success flow
- Swipe to pick item with quantity greater than 1 - API failure
- Swipe to pick item with invalid quantity selection
- ... and 15 more

## Navigation

- **PICKER_FLOW-01**: Navigate to the job details screen
- **PICKER_FLOW-03**: Navigate to the job details screen → Tap the Done button
- **PICKER_FLOW-08**: Navigate to the job details screen → Tap the OK button

## UI Elements

| Element | Mentions | Referenced In |
|---------|----------|---------------|
| Navigate to the job details (screen) | 20 | PICKER_FLOW-01, PICKER_FLOW-02, PICKER_FLOW-03, PICKER_FLOW-04, PICKER_FLOW-05 +15 |
| Amount picker (sheet) | 18 | PICKER_FLOW-02, PICKER_FLOW-03, PICKER_FLOW-04, PICKER_FLOW-05, PICKER_FLOW-06 +7 |
| Locate an (item) | 9 | PICKER_FLOW-01, PICKER_FLOW-02, PICKER_FLOW-03, PICKER_FLOW-04, PICKER_FLOW-05 +4 |
| Activate the (bar) | 8 | PICKER_FLOW-06, PICKER_FLOW-07, PICKER_FLOW-08, PICKER_FLOW-09, PICKER_FLOW-10 +3 |
| Scan the (bar) | 7 | PICKER_FLOW-06, PICKER_FLOW-07, PICKER_FLOW-08, PICKER_FLOW-09, PICKER_FLOW-10 +2 |
| Swipe the (item) | 5 | PICKER_FLOW-01, PICKER_FLOW-02, PICKER_FLOW-03, PICKER_FLOW-04, PICKER_FLOW-05 |
| code of an (item) | 5 | PICKER_FLOW-06, PICKER_FLOW-07, PICKER_FLOW-08, PICKER_FLOW-09, PICKER_FLOW-10 |
| Loading indicator appears in the job (item) | 4 | PICKER_FLOW-01, PICKER_FLOW-02, PICKER_FLOW-03, PICKER_FLOW-04 |
| Total area updates to reflect the picked (item) | 3 | PICKER_FLOW-01, PICKER_FLOW-03, PICKER_FLOW-06 |
| Error message is shown in the amount picker (sheet) | 2 | PICKER_FLOW-02, PICKER_FLOW-04 |
| Tap the Done (button) | 2 | PICKER_FLOW-03, PICKER_FLOW-04 |
| Error message is displayed in the amount picker (sheet) | 2 | PICKER_FLOW-07, PICKER_FLOW-09 |
| Tap the OK (button) | 2 | PICKER_FLOW-08, PICKER_FLOW-10 |
| Loading state appears in basket (item) | 2 | PICKER_FLOW-08, PICKER_FLOW-10 |
| Verify the (item) | 2 | PICKER_FLOW-11, PICKER_FLOW-12 |
| code of the (item) | 2 | PICKER_FLOW-11, PICKER_FLOW-12 |
| Tap the OK or Done (button) | 2 | PICKER_FLOW-11, PICKER_FLOW-12 |
| Amount picker displays current quantity for the (item) | 2 | PICKER_FLOW-11, PICKER_FLOW-12 |
| Observe the (item) | 1 | PICKER_FLOW-01 |
| Observe that amount picker (sheet) | 1 | PICKER_FLOW-03 |
| Select the desired amount in the amount picker (sheet) | 1 | PICKER_FLOW-04 |
| Done (button) | 1 | PICKER_FLOW-05 |
| Observe the amount picker (sheet) | 1 | PICKER_FLOW-06 |
| POST request is initiated with only (bar) | 1 | PICKER_FLOW-06 |
| Last scanned area below scanner shows the scanned (item) | 1 | PICKER_FLOW-06 |

## Behaviors

### Normal Flow (P0/P1)
- **PICKER_FLOW-01** [P0]: Swipe to pick item with quantity 1 - Success flow
  - Expected: Loading indicator appears in the job item price area; Swipe action is disabled during the request; Item is moved from Job section to Basket section af
- **PICKER_FLOW-03** [P0]: Swipe to pick item with quantity greater than 1 - Success flow
  - Expected: Amount picker sheet is displayed immediately after swipe; Amount picker sheet is dismissed immediately after tapping Done; Loading indicator appears i
- **PICKER_FLOW-06** [P0]: Scan barcode with quantity 1 - Success flow
  - Expected: Amount picker sheet appears immediately with loading state; POST request is initiated with only barcode in body; Amount picker sheet is dismissed auto
- **PICKER_FLOW-08** [P0]: Scan barcode with quantity greater than 1 - Success flow
  - Expected: Amount picker sheet appears immediately with loading state; Initial POST request completes successfully; Amount picker UI is shown for user to select 
- **PICKER_FLOW-11** [P0]: Scan barcode of item already in basket - Update quantity
  - Expected: Amount picker sheet appears immediately (not with loading state); Amount picker displays current quantity for the item; User can modify the quantity
- **PICKER_FLOW-14** [P1]: Remove item from basket - Existing functionality
  - Expected: Remove action is triggered successfully; DELETE or appropriate API request is sent; Item is removed from Basket section
- **PICKER_FLOW-16** [P1]: Replace item functionality - Existing functionality
  - Expected: Replace item UI is displayed; Available replacement options are shown; Selected replacement is processed via appropriate API
- **PICKER_FLOW-17** [P1]: Mark item as sold out - Existing functionality
  - Expected: Mark sold out action is triggered successfully; Appropriate API request is sent to mark item as unavailable; Item is removed from Job section or marke

### Edge Cases
- **PICKER_FLOW-18** [P2]: Total area displays spinner during basket GET call
  - When: User is logged in as a picker; User has an active job with items in the Basket section; Basket total needs to be refreshed

### Error States
- **PICKER_FLOW-02**: Swipe to pick item with quantity 1 - API failure
  - Expected: Loading indicator appears in the job item price area initially; Loading state stops when request fails; Amount picker sheet is displayed
- **PICKER_FLOW-04**: Swipe to pick item with quantity greater than 1 - API failure
  - Expected: Amount picker sheet dismisses after tapping Done; Loading indicator appears in the job item initially; Loading state stops when request fails
- **PICKER_FLOW-05**: Swipe to pick item with invalid quantity selection
  - Expected: Amount picker sheet is displayed after swipe; Done button is disabled when invalid amount is selected; User cannot proceed with amount of 0 or negativ
- **PICKER_FLOW-07**: Scan barcode with quantity 1 - API failure
  - Expected: Amount picker sheet appears with loading state; Loading state continues during API call; Error message is displayed in the amount picker sheet when re
- **PICKER_FLOW-09**: Scan barcode with quantity greater than 1 - Initial POST fails
  - Expected: Amount picker sheet appears with loading state; Loading state continues during POST API call; Error message is displayed in the amount picker sheet wh
- **PICKER_FLOW-10**: Scan barcode with quantity greater than 1 - PATCH fails after successful POST
  - Expected: Amount picker sheet appears with loading state initially; Amount picker UI is shown after successful POST; Amount picker dismisses after tapping OK
- **PICKER_FLOW-12**: Scan barcode of item already in basket - API failure during update
  - Expected: Amount picker sheet appears immediately; Amount picker displays current quantity for the item; User selects new quantity and taps OK/Done
- **PICKER_FLOW-13**: Scan invalid or unrecognized barcode
  - Expected: Scanner successfully reads the barcode; System attempts to match barcode with job items; Error message is displayed indicating barcode not found or no
- **PICKER_FLOW-15**: Update quantity on basket item manually - Existing functionality
  - Expected: Amount picker sheet is displayed with current quantity; User can increase or decrease the quantity; PATCH request is sent with new quantity
- **PICKER_FLOW-19**: Last scanned area shows loading state during API calls
  - Expected: Latest scanned or swiped item appears in Last scanned area immediately; Loading state (spinner or indicator) is displayed in Last scanned area during 

## API Dependencies

No API endpoints documented in test cases.

## Source Test Cases

- `Faster_Picker_Flow/FRA-876_Faster_Picker_Flow_KH_Stores.txt`
- Total: 20 test cases

<!-- MANUAL — Add your own notes below this line -->

## Manual Notes

<!-- Add accessibility IDs, navigation tips, tricky elements, etc. -->
