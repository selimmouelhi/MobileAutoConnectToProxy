# Share Shopping List

<!-- AUTO-EXTRACTED — Do not edit above this line manually -->
<!-- Extracted: 2026-04-01 14:24 | Source: 209 test cases -->

## Overview

Feature area covering 209 test cases. Key areas:
- Unshared list displays "Del liste" button instead of avatars
- Shared list displays avatars for users with access (2-3 people)
- Avatar overflow indicator shows "+x" when more than three people have access
- Avatars display initials fallback when a user has no profile picture
- Second and third avatar positions use distinct background colors
- ... and 204 more

## Navigation

- **SHARE_LIST-01**: User has navigated to a shopping list that is not shared with any other user → Tap the share list button
- **SHARE_LIST-02**: User has navigated to a shopping list shared with one or two other users (total 2 or 3 people including current user)
- **SHARE_LIST-03**: User has navigated to a shopping list shared with three or more other users (total 4+ people including current user)
- **SHARE_LIST-04**: User has navigated to a shopping list shared with at least one other user
- **SHARE_LIST-05**: User has navigated to a shopping list shared with at least two other users (total 3+ people)
- **SHARE_LIST-06**: User has navigated to a shopping list shared with at least one other user → Tap and hold on the avatar area briefly to observe the pressed state before releasing → Release the tap on the avatar area
- **SHARE_LIST-07**: User has navigated to a shopping list shared with at least one other user → Tap the "Del liste" button while the access data is still loading
- **SHARE_LIST-08**: Navigate to the shopping list screen and note the avatars currently displayed → Navigate away from the shopping list screen → Navigate back to the shopping list screen
- **SHARE_LIST-09**: User has navigated to a shopping list screen → Tap the share list button
- **SHARE_LIST-10**: User has navigated to a shopping list shared with at least one other user → Tap the avatars

## UI Elements

| Element | Mentions | Referenced In |
|---------|----------|---------------|
| Who has access | 32 | COMPAT-09, COMPAT-10, QR_CODE-09, WHO_ACCESS-01, WHO_ACCESS-02 +13 |
| Observe the (sheet) | 26 | SHARE_LIST-01, SHARE_LIST-02, SHARE_LIST-03, SHARE_LIST-04, SHARE_LIST-05 +14 |
| invitation (sheet) | 26 | ACCEPT_INV-01, ACCEPT_INV-02, ACCEPT_INV-05, ACCEPT_INV-09, ACCEPT_INV-10 +20 |
| Observe the (screen) | 20 | ACCEPT_INV-01, ACCEPT_INV-02, ACCEPT_INV-18, ACCEPT_INV-19, ACCEPT_INV-20 +15 |
| Del liste | 18 | SHARE_LIST-01, SHARE_LIST-02, SHARE_LIST-06, SHARE_LIST-07, SHARE_LIST-21 +3 |
| share shopping list (sheet) | 16 | QR_CODE-04, QR_CODE-08, QR_CODE-09, QR_CODE-10, QR_CODE-28 +9 |
| The (button) | 15 | QR_CODE-02, QR_CODE-14, QR_CODE-20, QR_CODE-23, QR_CODE-25 +5 |
| Observe the (button) | 12 | QR_CODE-01, QR_CODE-03, QR_CODE-20, QR_CODE-23, QR_CODE-25 +7 |
| Observe the share area on the shopping list (screen) | 10 | SHARE_LIST-01, SHARE_LIST-02, SHARE_LIST-03, SHARE_LIST-07, SHARE_LIST-16 +5 |
| Tap the share list (button) | 10 | SHARE_LIST-01, SHARE_LIST-03, SHARE_LIST-09, SHARE_LIST-14, SHARE_LIST-17 +3 |
| The (sheet) | 10 | ACCEPT_INV-36, SHARE_LIST-17, SHARE_LIST-30, WHO_ACCESS-06, WHO_ACCESS-10 +1 |
| Observe the invitation (sheet) | 9 | ACCEPT_INV-05, ACCEPT_INV-06, ACCEPT_INV-11, ACCEPT_INV-13, ACCEPT_INV-15 +4 |
| Luk | 8 | QR_CODE-07, QR_CODE-08, QR_CODE-09, QR_CODE-10, QR_CODE-12 +3 |
| confirmation (sheet) | 8 | WHO_ACCESS-14, WHO_ACCESS-18, WHO_ACCESS-19, WHO_ACCESS-20, WHO_ACCESS-21 |
| Tap the Share (link) | 8 | SHARE_LINK-04, SHARE_LINK-06, SHARE_LINK-07, SHARE_LINK-11, SHARE_LINK-14 +3 |
| Navigate to the shopping list (screen) | 7 | SHARE_LIST-08, SHARE_LIST-16, SHARE_LIST-19, SHARE_LIST-28, SHARE_LIST-29 +1 |
| Fjern | 7 | WHO_ACCESS-13, WHO_ACCESS-14, WHO_ACCESS-23, WHO_ACCESS-24 |
| OK | 7 | QR_CODE-03, QR_CODE-04, SHARE_LINK-11, SHARE_LINK-12, SHARE_LINK-13 +2 |
| Tap the Copy (link) | 7 | SHARE_LINK-05, SHARE_LINK-10, SHARE_LINK-12, SHARE_LINK-14, SHARE_LINK-15 +2 |
| s on the shopping list (screen) | 6 | SHARE_LIST-04, SHARE_LIST-05, SHARE_LIST-10, SHARE_LIST-24, SHARE_LIST-25 |
| Tap the X (button) | 6 | ACCEPT_INV-09, SHARE_LIST-06, SHARE_LIST-12, SHARE_LIST-18, WHO_ACCESS-12 |
| Shopping list (screen) | 6 | SHARE_LIST-06, SHARE_LIST-07, SHARE_LIST-12, SHARE_LIST-13, SHARE_LIST-19 +1 |
| Observe the share (sheet) | 6 | SHARE_LIST-17, SHARE_LIST-19, SHARE_LIST-20, SHARE_LIST-30, SHARE_LIST-32 +1 |
| Der skete en fejl | 6 | QR_CODE-03, SHARE_LINK-11, SHARE_LINK-12, SHARE_LIST-18, SHARE_LIST-31 +1 |
| Tap the retry (button) | 6 | SHARE_LIST-20, SHARE_LIST-21, SHARE_LIST-33, SHARE_LIST-34 |

## Behaviors

### Normal Flow (P0/P1)
- **SHARE_LIST-01** [P0]: Unshared list displays "Del liste" button instead of avatars
  - Expected: The share list button labeled "Del liste" is displayed in the share area; No avatar icons are visible anywhere on the shopping list screen; Tapping "D
- **SHARE_LIST-02** [P0]: Shared list displays avatars for users with access (2-3 people)
  - Expected: Avatar icons are displayed instead of the "Del liste" button; The current user's avatar is shown first (leftmost position); Remaining avatars are sort
- **SHARE_LIST-03** [P0]: Avatar overflow indicator shows "+x" when more than three people have access
  - Expected: Exactly two individual avatar icons are displayed (current user first, then the next user alphabetically); The third position displays an overflow ind
- **SHARE_LIST-04** [P0]: Avatars display initials fallback when a user has no profile picture
  - Expected: The avatar for the user without a profile picture displays their initials (first letter of first name + first letter of last name); The initials are c
- **SHARE_LIST-05** [P1]: Second and third avatar positions use distinct background colors
  - Expected: The background color of the second-position avatar differs from the first-position avatar; The background color of the third-position avatar or overfl
- **SHARE_LIST-06** [P0]: Tapping avatars produces a highlight state and presents the share sheet
  - Expected: The avatar icons display a visible highlight or pressed state while the tap is held; Upon release the share shopping list bottom sheet is presented; S
- **SHARE_LIST-08** [P1]: Avatars update to reflect current shared users each time the screen is presented
  - Expected: On the first visit the avatar count and identities reflect the original number of shared users; On the second visit the avatar area updates to include
- **SHARE_LIST-09** [P0]: Present share sheet via share list button
  - Expected: Share shopping list bottom sheet is presented over the current screen; Sheet header displays the title matching localization key app_share_list.title;
- **SHARE_LIST-10** [P0]: Present share sheet via avatars
  - Expected: Share shopping list bottom sheet is presented over the current screen; Sheet header displays the title matching localization key app_share_list.title;
- **SHARE_LIST-11** [P0]: Sheet shows loading state with Rema spinner when data is not yet fetched
  - Expected: Sheet is presented successfully while data is still loading; Full sheet loading state is displayed with the Rema spinner centered in the sheet; No par

### Edge Cases
- **SHARE_LIST-07** [P1]: Share area transitions from "Del liste" to avatars after access data loads
  - When: User is logged in to the Rema 1000 app; User has navigated to a shopping list shared with at least one other user; The fetch of who has access has not
- **SHARE_LIST-18** [P2]: Share sheet dismiss button (X) is visually consistent and accessible
  - When: User is logged in to the Rema 1000 app; Share shopping list bottom sheet is currently presented
- **SHARE_LIST-27** [P1]: Share area transitions smoothly from "Del liste" to avatars after access data loads
  - When: User is logged in to the Rema 1000 app; User has navigated to a shopping list that is shared with at least one other user; The fetch of who has access
- **QR_CODE-11** [P0]: QR code screen prevents the phone from going to sleep
  - When: User is logged in to the Rema 1000 app; Device auto-lock / screen timeout is set to a short duration (e.g. 30 seconds); QR code screen is displayed
- **QR_CODE-12** [P1]: Phone sleep prevention is removed when QR code screen is closed
  - When: User is logged in to the Rema 1000 app; QR code screen is displayed; Device auto-lock / screen timeout is set to a short duration (e.g. 30 seconds)
- **ACCEPT_INV-03** [P0]: Deep link is ignored when cookie consent prompt is showing
  - When: Rema 1000 app is installed on the device; User has not yet made a decision on cookies (cookie consent prompt is showing)
- **ACCEPT_INV-17** [P0]: Invitation sheet shows login required body when user is not logged in
  - When: User is NOT logged in to the Rema 1000 app; User has completed the cookie consent flow; User taps a valid deep link
- **ACCEPT_INV-18** [P0]: Tapping login button dismisses invitation sheet and opens login flow
  - When: User is NOT logged in to the Rema 1000 app; Invitation sheet is displayed with the login required state
- **ACCEPT_INV-19** [P0]: Tapping create user button dismisses invitation sheet and opens create user flow
  - When: User is NOT logged in to the Rema 1000 app; Invitation sheet is displayed with the login required state
- **ACCEPT_INV-20** [P0]: Invitation flow resumes after user logs in
  - When: User was NOT logged in and tapped a valid deep link; Invitation sheet was presented and user tapped the login button; Login flow is in progress

### Error States
- **SHARE_LIST-12**: Dismiss share sheet by tapping the X button
  - Expected: Sheet dismisses immediately upon tapping X; Dismiss animation plays smoothly; User returns to the shopping list screen
- **SHARE_LIST-13**: Dismiss share sheet by tapping outside the sheet
  - Expected: Sheet dismisses when tapping outside its boundaries; Dismiss animation plays smoothly; User returns to the shopping list screen
- **SHARE_LIST-17**: Share sheet stays on loading state when fetch who has access fails
  - Expected: The share shopping list sheet is presented successfully; The sheet displays the full loading state with the Rema spinner while the request is in fligh
- **SHARE_LIST-18**: Error alert displays correct title, message, and action buttons on fetch failure
  - Expected: An error alert is presented on top of the share shopping list sheet; The alert title displays the text defined by localization key app_share_list.who_
- **SHARE_LIST-19**: Tapping dismiss button on error alert closes both the alert and the share sheet
  - Expected: The error alert is dismissed immediately upon tapping the dismiss button; The share shopping list sheet is also dismissed as a direct result of tappin
- **SHARE_LIST-20**: Tapping retry button dismisses alert and retries the request with sheet still open
  - Expected: The error alert is dismissed immediately upon tapping the retry button; The share shopping list sheet remains open and returns to the full loading sta
- **SHARE_LIST-21**: Successive retry failures do not degrade sheet state or responsiveness
  - Expected: Each retry cycle follows the same sequence: alert is dismissed, sheet returns to loading state, a new request is fired, and the alert reappears on fai
- **SHARE_LIST-06**: Dismiss share sheet by tapping the X button
  - Expected: Sheet dismisses immediately upon tapping X; Dismiss animation plays smoothly; User returns to the shopping list screen
- **SHARE_LIST-07**: Dismiss share sheet by tapping outside the sheet
  - Expected: Sheet dismisses when tapping outside its boundaries; Dismiss animation plays smoothly; User returns to the shopping list screen
- **SHARE_LIST-09**: Deep link opens app and navigates to shopping list invitation - iOS
  - Expected: iOS system recognizes the deep link and opens the Rema 1000 app; App opens directly without requiring the user to launch it manually; App navigates to

## API Dependencies

| Method | Endpoint | Description | Used In |
|--------|----------|-------------|---------|
| POST | `/api/v3/invitation-links/{id}` | Legacy auto-accept flow | COMPAT-01, COMPAT-02, COMPAT-04 |
| GET | `/api/v1/shoppinglists/polling` | Syncs shared list data | COMPAT-01, COMPAT-02, COMPAT-03, COMPAT-04, COMPAT-05 +5 |
| GET | `/api/v3/users/{id}/shopping-list-invitations` | Shows pending invitation before auto-accept | COMPAT-02, COMPAT-05, COMPAT-06 |
| DELETE | `/api/v1/shoppinglists/{id}` | User B removes access | COMPAT-09 |
| DELETE | `/api/v3/shopping-lists/{id}/members/{userId}` | Revoke access | COMPAT-10 |
| GET | `/api/shopping-lists/{id}` | Returns shopping list with shared users data | WHO_ACCESS-01, WHO_ACCESS-02, WHO_ACCESS-03, WHO_ACCESS-04, WHO_ACCESS-05 +5 |

## Platform Notes

### iOS-Specific
- **SHARE_LIST-09**: Deep link opens app and navigates to shopping list invitation - iOS
- **SHARE_LIST-15**: Verify KMP shared code compiles and runs on iOS
- **COMPAT-03**: v6.4 user receives invitation - Verify user-agent detection
- **COMPAT-07**: v6.4 user-agent spoofing - Verify backend validation

### Android-Specific
- **SHARE_LIST-10**: Deep link opens app and navigates to shopping list invitation - Android

## Source Test Cases

- `Share_Shopping_List/SHARE_LIST_Module1_Share_Shopping_List_Sheet.txt`
- `Share_Shopping_List/SHARE_LIST_Module1_UI_Foundation_Infrastructure.txt`
- `Share_Shopping_List/SHARE_LIST_Module2_Who_Has_Access.txt`
- `Share_Shopping_List/SHARE_LIST_Module3_Share_Link.txt`
- `Share_Shopping_List/SHARE_LIST_Module4_QR_Code.txt`
- `Share_Shopping_List/SHARE_LIST_Module5_Accept_Invitation.txt`
- `Share_Shopping_List/SHARE_LIST_Backward_Compatibility_v6.4_v6.5.txt`
- `Share_Shopping_List/SHARE_LIST_Summary.txt`
- `Share_Shopping_List/FRA-747_View_Who_Has_Access.txt`
- Total: 209 test cases

<!-- MANUAL — Add your own notes below this line -->

## Manual Notes

<!-- Add accessibility IDs, navigation tips, tricky elements, etc. -->
