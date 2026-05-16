# Cookie Consent

<!-- AUTO-EXTRACTED — Do not edit above this line manually -->
<!-- Extracted: 2026-04-01 14:24 | Source: 20 test cases -->

## Overview

Feature area covering 20 test cases. Key areas:
- Verify cookie prompt appears on fresh app install
- Verify cookie prompt appears after app update for existing users
- Verify accepting all cookies dismisses prompt
- Verify accepting only necessary cookies dismisses prompt
- Verify opening cookie preferences configuration screen
- ... and 15 more

## Navigation

- **cookie_prompt-01**: Launch the app for the first time
- **cookie_prompt-02**: Open the updated app
- **cookie_prompt-03**: Tap "Det er OK" button
- **cookie_prompt-04**: Tap "Kun nødvendige" button
- **cookie_prompt-05**: Tap "Indstil præferencer" button
- **cookie_prompt-06**: User is on cookie preferences configuration screen → "Nødvendige" toggle is ON → Tap on "Nødvendige" toggle to attempt turning it OFF
- **cookie_prompt-07**: User is on cookie preferences configuration screen → Tap "Funktionelle - fejlsøgning" toggle to turn it ON → Tap "Accepter valgte" button
- **cookie_prompt-08**: User is on cookie preferences configuration screen → Tap "Accepter alle" button
- **cookie_prompt-09**: Tap "Læs mere om vores persondatapolitik" link
- **cookie_prompt-10**: Tap "Læs mere" link in cookie description text

## UI Elements

| Element | Mentions | Referenced In |
|---------|----------|---------------|
| Observe the (screen) | 6 | cookie_prompt-02, cookie_prompt-03, cookie_prompt-04, cookie_prompt-07, cookie_prompt-08 +1 |
| Funktionelle - fejlsøgning | 6 | cookie_prompt-05, cookie_prompt-07, cookie_settings-02, cookie_settings-04, cookie_settings-05 |
| Nødvendige | 5 | cookie_prompt-05, cookie_prompt-06, cookie_settings-02, cookie_settings-03 |
| Cookie consent bottom (sheet) | 4 | cookie_prompt-01, cookie_prompt-02, cookie_prompt-03, cookie_prompt-04 |
| Cookie (prompt) | 4 | cookie_prompt-03, cookie_prompt-04, cookie_prompt-07, cookie_prompt-08 |
| Det er OK | 3 | cookie_prompt-01, cookie_prompt-03, cookie_prompt-11 |
| Configuration (screen) | 3 | cookie_prompt-05, cookie_prompt-07, cookie_prompt-08 |
| Cookies hjælper os med at forbedre appen | 2 | cookie_prompt-01, cookie_prompt-05 |
| Bottom (sheet) | 2 | cookie_prompt-01, cookie_prompt-02 |
| Kun nødvendige | 2 | cookie_prompt-01, cookie_prompt-04 |
| Indstil præferencer | 2 | cookie_prompt-01, cookie_prompt-05 |
| Læs mere om vores persondatapolitik | 2 | cookie_prompt-01, cookie_prompt-09 |
| Læs mere | 2 | cookie_prompt-01, cookie_prompt-10 |
| User proceeds to the welcome (screen) | 2 | cookie_prompt-03, cookie_prompt-04 |
| Accepter valgte | 2 | cookie_prompt-05, cookie_prompt-07 |
| Accepter alle | 2 | cookie_prompt-05, cookie_prompt-08 |
| User proceeds to welcome (screen) | 2 | cookie_prompt-07, cookie_prompt-08 |
| User can navigate back to cookie (prompt) | 2 | cookie_prompt-09, cookie_prompt-10 |
| Cookie consent (prompt) | 2 | cookie_prompt-12, cookie_prompt-13 |
| Observe the bottom (sheet) | 1 | cookie_prompt-01 |
| is displayed on top of welcome (screen) | 1 | cookie_prompt-01 |
| Three action (button) | 1 | cookie_prompt-01 |
| appears on top of the current (screen) | 1 | cookie_prompt-02 |
| All cookie (prompt) | 1 | cookie_prompt-02 |
| Observe the new (screen) | 1 | cookie_prompt-05 |

## Behaviors

### Normal Flow (P0/P1)
- **cookie_prompt-11** [P1]: Verify ATT prompt appears after cookie consent on iOS
  - Expected: ATT (App Tracking Transparency) prompt appears; Prompt text is displayed in Danish; Prompt contains options to allow or deny tracking

### Edge Cases
- **cookie_prompt-01**: Verify cookie prompt appears on fresh app install
  - When: User has never installed the app before; App is freshly installed on device
- **cookie_prompt-02**: Verify cookie prompt appears after app update for existing users
  - When: User has app installed from version before cookie prompt feature; App is updated to version with cookie prompt feature
- **cookie_prompt-03**: Verify accepting all cookies dismisses prompt
  - When: User has freshly installed app; Cookie consent prompt is displayed
- **cookie_prompt-04**: Verify accepting only necessary cookies dismisses prompt
  - When: User has freshly installed app; Cookie consent prompt is displayed
- **cookie_prompt-05**: Verify opening cookie preferences configuration screen
  - When: User has freshly installed app; Cookie consent prompt is displayed
- **cookie_prompt-07**: Verify enabling functional cookies and accepting selection
  - When: User is on cookie preferences configuration screen; "Funktionelle - fejlsøgning" toggle is OFF by default
- **cookie_prompt-08**: Verify accepting all cookies from configuration screen
  - When: User is on cookie preferences configuration screen
- **cookie_prompt-09**: Verify privacy policy link opens correctly
  - When: User has freshly installed app; Cookie consent prompt is displayed
- **cookie_prompt-10**: Verify cookie information link opens correctly
  - When: User has freshly installed app; Cookie consent prompt is displayed
- **cookie_prompt-12**: Verify cookie prompt does not reappear after accepting
  - When: User has accepted cookies in previous session; App was closed completely

### Error States
- **cookie_prompt-06**: Verify necessary cookies toggle cannot be disabled
  - Expected: "Nødvendige" toggle remains ON; Toggle does not respond to tap interaction; No error message is displayed

## API Dependencies

No API endpoints documented in test cases.

## Platform Notes

### iOS-Specific
- **cookie_prompt-11**: Verify ATT prompt appears after cookie consent on iOS

## Source Test Cases

- `Cookie_Consent/cookie_prompt_test_cases.txt`
- `Cookie_Consent/cookie_settings_test_cases.txt`
- Total: 20 test cases

<!-- MANUAL — Add your own notes below this line -->

## Manual Notes

<!-- Add accessibility IDs, navigation tips, tricky elements, etc. -->
