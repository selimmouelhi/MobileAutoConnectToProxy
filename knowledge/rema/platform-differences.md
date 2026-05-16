# Rema App — Platform Differences (iOS vs Android)

<!-- AUTO-EXTRACTED -->
<!-- Extracted: 2026-04-01 14:24 -->

## General Notes

- iOS uses `XCUIElementType*` classes in Appium page source
- Android uses `android.widget.*` and `android.view.*` classes
- Element finding strategies differ:
  - iOS: `accessibility id`, `//XCUIElementTypeStaticText[@name='X']`, `//*[contains(@label, 'X')]`
  - Android: `accessibility id`, `//*[contains(@text, 'X')]`, `//*[contains(@content-desc, 'X')]`

## iOS-Specific Test Cases

### Share Shopping List
- **SHARE_LIST-09**: Deep link opens app and navigates to shopping list invitation - iOS
- **SHARE_LIST-15**: Verify KMP shared code compiles and runs on iOS
- **COMPAT-03**: v6.4 user receives invitation - Verify user-agent detection
- **COMPAT-07**: v6.4 user-agent spoofing - Verify backend validation

### Favorite Recipes
- **FAVREC-28**: Verify dismiss icon size and alignment on recipe details (iOS-specific)

### Payment Methods
- **FRA-09**: Click & Collect flow respects feature flags

### Vigo
- **VIGO-16**: Verify login flow works correctly - iOS

### Cookie Consent
- **cookie_prompt-11**: Verify ATT prompt appears after cookie consent on iOS

### FAQ Help Page
- **faq_help_page-05**: iOS device uses Safari view controller

## Android-Specific Test Cases

### Share Shopping List
- **SHARE_LIST-10**: Deep link opens app and navigates to shopping list invitation - Android

### Payment Methods
- **FRA-01**: Both payment methods enabled - Happy path selection
- **FRA-02**: MobilePay disabled via feature flag
- **FRA-03**: Worldline disabled via feature flag
- **FRA-04**: Both payment methods disabled via feature flags
- **FRA-05**: Feature flag refresh when app returns from background
- **FRA-08**: Bottom sheet dismissal preserves feature flag state

### Vigo
- **VIGO-06**: Verify Settings title changed to "Indstillinger" on Android
- **VIGO-15**: Verify login flow works correctly - Android

### FAQ Help Page
- **faq_help_page-04**: Android device uses Chrome Custom Tabs

<!-- MANUAL -->

## Manual Notes

<!-- Add real Appium selector differences, platform-specific bugs, etc. -->
