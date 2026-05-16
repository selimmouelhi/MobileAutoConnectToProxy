# Payment Methods

<!-- AUTO-EXTRACTED — Do not edit above this line manually -->
<!-- Extracted: 2026-04-01 14:24 | Source: 10 test cases -->

## Overview

Feature area covering 10 test cases. Key areas:
- Both payment methods enabled - Happy path selection
- MobilePay disabled via feature flag
- Worldline disabled via feature flag
- Both payment methods disabled via feature flags
- Feature flag refresh when app returns from background
- ... and 5 more

## Navigation

- **FRA-01**: Navigate to checkout screen → Tap the payment method selector → Tap confirm/continue to proceed with checkout
- **FRA-02**: Navigate to checkout screen → Tap the payment method selector
- **FRA-05**: Navigate back to checkout screen → Tap the payment method selector
- **FRA-08**: Navigate to checkout screen → Tap the payment method selector → Tap the payment method selector again
- **FRA-09**: Navigate to Click & Collect checkout screen → Tap the payment method selector
- **FRA-10**: Navigate to checkout screen on iOS device → Tap the payment method selector

## UI Elements

| Element | Mentions | Referenced In |
|---------|----------|---------------|
| Tap the payment method (selector) | 11 | FRA-01, FRA-02, FRA-03, FRA-04, FRA-05 +5 |
| Observe the payment method bottom (sheet) | 9 | FRA-01, FRA-02, FRA-03, FRA-04, FRA-05 +4 |
| Payment method bottom (sheet) | 9 | FRA-01, FRA-02, FRA-03, FRA-04, FRA-05 +4 |
| Navigate to checkout (screen) | 8 | FRA-01, FRA-02, FRA-03, FRA-04, FRA-06 +3 |
| Both MobilePay and Worldline (button) | 3 | FRA-01, FRA-04, FRA-06 |
| MobilePay (button) | 2 | FRA-02, FRA-03 |
| Worldline (button) | 2 | FRA-02, FRA-03 |
| Select MobilePay from the bottom (sheet) | 1 | FRA-01 |
| MobilePay kan ikke benyttes i øjeblikket. Benyt et andet betalingsmiddel. | 1 | FRA-02 |
| Betalingskort kan ikke benyttes i øjeblikket. Benyt et andet betalingsmiddel. | 1 | FRA-03 |
| Det er ikke muligt at lave ordre i øjeblikket. Prøv venligst igen senere. | 1 | FRA-04 |
| Navigate back to checkout (screen) | 1 | FRA-05 |
| Feature flags are re-fetched when bottom (sheet) | 1 | FRA-05 |
| Observe Worldline disabled state in bottom (sheet) | 1 | FRA-08 |
| Dismiss the bottom (sheet) | 1 | FRA-08 |
| Bottom (sheet) | 1 | FRA-08 |
| Collect checkout (screen) | 1 | FRA-09 |

## Behaviors

### Edge Cases
- **FRA-01**: Both payment methods enabled - Happy path selection
  - When: User is logged in and has items in cart; Feature flags app.android.payments.mobilePay and app.android.payments.worldline are set to true
- **FRA-02**: MobilePay disabled via feature flag
  - When: User is logged in and has items in cart; Feature flag app.android.payments.mobilePay is set to false; Feature flag app.android.payments.worldline is s
- **FRA-03**: Worldline disabled via feature flag
  - When: User is logged in and has items in cart; Feature flag app.android.payments.mobilePay is set to true; Feature flag app.android.payments.worldline is se
- **FRA-05**: Feature flag refresh when app returns from background
  - When: User is logged in with items in cart; Payment method bottom sheet was previously shown with both methods enabled; User sends app to background
- **FRA-07**: Feature flags missing from API response
  - When: User is logged in and has items in cart; Feature flag API returns success but payment method flags are not included in response
- **FRA-08**: Bottom sheet dismissal preserves feature flag state
  - When: User is logged in with items in cart; Feature flag app.android.payments.worldline is set to false
- **FRA-09**: Click & Collect flow respects feature flags
  - When: User is logged in with items in cart; User has selected Click & Collect delivery method; Feature flag app.ios.payments.mobilePay is set to false
- **FRA-10**: Platform-specific feature flag isolation
  - When: User is logged in with items in cart; On iOS platform; Feature flag app.ios.payments.mobilePay is set to false

### Error States
- **FRA-04**: Both payment methods disabled via feature flags
  - Expected: Payment method bottom sheet displays; Both MobilePay and Worldline buttons show disabled state; Critical error message displays: "Det er ikke muligt a
- **FRA-06**: API failure defaults to payment methods enabled
  - Expected: Payment method bottom sheet displays despite API failure; Both MobilePay and Worldline buttons are enabled (default behavior); No disabled state messa

## API Dependencies

| Method | Endpoint | Description | Used In |
|--------|----------|-------------|---------|
| GET | `/api/feature-flags` | Returns mobilePay and worldline flags as true | FRA-01, FRA-02, FRA-03, FRA-04, FRA-05 +5 |

## Feature Flags

- `app.android.payments.mobilePay` — referenced in FRA-01, FRA-02, FRA-03, FRA-04, FRA-05
- `app.android.payments.worldline` — referenced in FRA-01, FRA-02, FRA-03, FRA-04, FRA-08
- `app.ios.payments.mobilePay` — referenced in FRA-09, FRA-10

## Platform Notes

### iOS-Specific
- **FRA-09**: Click & Collect flow respects feature flags

### Android-Specific
- **FRA-01**: Both payment methods enabled - Happy path selection
- **FRA-02**: MobilePay disabled via feature flag
- **FRA-03**: Worldline disabled via feature flag
- **FRA-04**: Both payment methods disabled via feature flags
- **FRA-05**: Feature flag refresh when app returns from background

## Source Test Cases

- `Payment_Methods/FRA-220_Payment_Methods_Feature_Flags.txt`
- Total: 10 test cases

<!-- MANUAL — Add your own notes below this line -->

## Manual Notes

<!-- Add accessibility IDs, navigation tips, tricky elements, etc. -->
