# FAQ Help Page

<!-- AUTO-EXTRACTED — Do not edit above this line manually -->
<!-- Extracted: 2026-04-01 14:24 | Source: 12 test cases -->

## Overview

Feature area covering 12 test cases. Key areas:
- FAQ button is visible on all relevant screens
- FAQ button stays in place when clicked (no animation)
- In-app browser opens with correct help page URL
- Android device uses Chrome Custom Tabs
- iOS device uses Safari view controller
- ... and 7 more

## Navigation

- **faq_help_page-01**: Navigate to the main screen → Navigate to each screen that previously had the FAQ button
- **faq_help_page-02**: User is on any screen with the FAQ button visible → Tap the FAQ button → Observe the button's position during and after the tap
- **faq_help_page-03**: User is on any screen with the FAQ button visible → Tap the FAQ button
- **faq_help_page-04**: User is on any screen with the FAQ button visible → Tap the FAQ button → Observe the browser interface that opens
- **faq_help_page-06**: User has opened the help page via the FAQ button
- **faq_help_page-07**: User has opened the help page via the FAQ button → Navigate to multiple pages within the help site (click internal links)
- **faq_help_page-08**: Open FAQ from the first screen with FAQ button → Navigate to a different screen with FAQ button → Open FAQ from the second screen
- **faq_help_page-09**: Navigate to the first screen with FAQ button → Navigate to the second screen with FAQ button
- **faq_help_page-10**: User is on any screen with the FAQ button visible → Tap the FAQ button quickly → Tap the FAQ button again → Measure the time from tap to browser opening

## UI Elements

| Element | Mentions | Referenced In |
|---------|----------|---------------|
| FAQ (button) | 10 | faq_help_page-01, faq_help_page-02, faq_help_page-06, faq_help_page-09, faq_help_page-10 +1 |
| Tap the FAQ (button) | 7 | faq_help_page-02, faq_help_page-03, faq_help_page-04, faq_help_page-05, faq_help_page-10 +1 |
| with FAQ (button) | 4 | faq_help_page-08, faq_help_page-09 |
| Observe the (button) | 3 | faq_help_page-02, faq_help_page-12 |
| Note the exact position of FAQ (button) | 2 | faq_help_page-09 |
| Navigate to the main (screen) | 1 | faq_help_page-01 |
| Observe the bottom left corner of the (screen) | 1 | faq_help_page-01 |
| Navigate to each (screen) | 1 | faq_help_page-01 |
| that previously had the FAQ (button) | 1 | faq_help_page-01 |
| is visible in the bottom left corner on all relevant (screen) | 1 | faq_help_page-01 |
| appearance is consistent across all (screen) | 1 | faq_help_page-01 |
| Locate the FAQ (button) | 1 | faq_help_page-02 |
| does NOT animate or move to the top of the (screen) | 1 | faq_help_page-02 |
| Check the URL in the browser address (bar) | 1 | faq_help_page-03 |
| In-app browser opens immediately after tapping FAQ (button) | 1 | faq_help_page-03 |
| Chrome Custom (tab) | 1 | faq_help_page-04 |
| address (bar) | 1 | faq_help_page-04 |
| Safari browser UI is visible with address (bar) | 1 | faq_help_page-05 |
| Done | 1 | faq_help_page-05 |
| Close the browser using the platform-specific close (button) | 1 | faq_help_page-06 |
| Done (button) | 1 | faq_help_page-06 |
| back (button) | 1 | faq_help_page-06 |
| Observe the (screen) | 1 | faq_help_page-06 |
| User returns to the original (screen) | 1 | faq_help_page-06 |
| where FAQ (button) | 1 | faq_help_page-06 |

## Behaviors

### Normal Flow (P0/P1)
- **faq_help_page-01** [P0]: FAQ button is visible on all relevant screens
  - Expected: FAQ button is visible in the bottom left corner on all relevant screens; FAQ button appearance is consistent across all screens; FAQ button is properl
- **faq_help_page-02** [P0]: FAQ button stays in place when clicked (no animation)
  - Expected: FAQ button remains in the bottom left corner when tapped; FAQ button shows a highlight or pressed state when tapped; FAQ button does NOT animate or mo
- **faq_help_page-03** [P0]: In-app browser opens with correct help page URL
  - Expected: In-app browser opens immediately after tapping FAQ button; URL displayed is https://madogdrikke.rema1000.dk; Help page content loads and is displayed 
- **faq_help_page-04** [P1]: Android device uses Chrome Custom Tabs
  - Expected: Chrome Custom Tabs interface opens; Chrome browser UI is visible (address bar, menu options); Chrome branding or indicators are present
- **faq_help_page-05** [P1]: iOS device uses Safari view controller
  - Expected: SFSafariViewController interface opens; Safari browser UI is visible with address bar; "Done" button is visible in the top corner
- **faq_help_page-06** [P0]: User can close browser and return to app
  - Expected: Browser closes successfully; User returns to the original screen where FAQ button was tapped; Original screen state is preserved (no data loss or rese
- **faq_help_page-07** [P1]: App state preserved after navigating within help page
  - Expected: User can navigate freely within the help site; Browser navigation works correctly (back/forward buttons); After closing browser, user returns to origi
- **faq_help_page-08** [P1]: FAQ button opens same URL from multiple screens
  - Expected: Same URL (https://madogdrikke.rema1000.dk) opens from all screens; Help page content is identical regardless of which screen FAQ was opened from; No s

### Edge Cases
- **faq_help_page-09** [P2]: FAQ button position consistent across screens
  - When: User is logged into the app; User has access to multiple screens with FAQ button
- **faq_help_page-10** [P2]: FAQ button tap responsiveness
  - When: User is on any screen with the FAQ button visible
- **faq_help_page-12** [P2]: FAQ button visual highlight state
  - When: User is on any screen with the FAQ button visible

### Error States
- **faq_help_page-11**: FAQ functionality works without internet connection
  - Expected: FAQ button remains visible and tappable; Browser attempts to open; Appropriate error message is displayed indicating no internet connection

## API Dependencies

No API endpoints documented in test cases.

## Platform Notes

### iOS-Specific
- **faq_help_page-05**: iOS device uses Safari view controller

### Android-Specific
- **faq_help_page-04**: Android device uses Chrome Custom Tabs

## Source Test Cases

- `FAQ_Help_Page/faq_help_page_test_cases.txt`
- Total: 12 test cases

<!-- MANUAL — Add your own notes below this line -->

## Manual Notes

<!-- Add accessibility IDs, navigation tips, tricky elements, etc. -->
