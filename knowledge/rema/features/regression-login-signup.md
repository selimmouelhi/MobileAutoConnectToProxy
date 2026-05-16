# User Login & Signup

<!-- AUTO-EXTRACTED — Do not edit above this line manually -->
<!-- Extracted: 2026-04-01 14:24 | Source: 7 test cases -->

## Overview

Feature area covering 7 test cases. Key areas:
- Sign up flow > Create a new user after tapping on order flow
- Login flow > Login after tapping on order flow
- Login flow > Login with shopper who does not have free delivery
- Delete user
- Logout while preselecting list
- ... and 2 more

## Navigation

- **REG02-01**: Tap on order flow → Tap on login/opret bruger
- **REG02-02**: Tap on order flow → Tap on the left of cancel button → Tap on login/opret bruger
- **REG02-03**: Tap on login
- **REG02-05**: Open front page

## UI Elements

| Element | Mentions | Referenced In |
|---------|----------|---------------|
| Add (item) | 3 | REG02-01, REG02-02, REG02-06 |
| Tap on the left of cancel (button) | 1 | REG02-02 |
| user is unable to choose users  from test (menu) | 1 | REG02-02 |
| User is able to order (item) | 1 | REG02-06 |

## Behaviors

### Edge Cases
- **REG02-01**: Sign up flow > Create a new user after tapping on order flow
- **REG02-02**: Login flow > Login after tapping on order flow
- **REG02-03**: Login flow > Login with shopper who does not have free delivery
- **REG02-04**: Delete user
- **REG02-05**: Logout while preselecting list
- **REG02-06**: User mitid verification [Test on preprod] > Verify mitID
- **REG02-07**: Edit user informations

## API Dependencies

No API endpoints documented in test cases.

## Source Test Cases

- `Regression_Tests/02_create_new_user_login.txt`
- Total: 7 test cases

<!-- MANUAL — Add your own notes below this line -->

## Manual Notes

<!-- Add accessibility IDs, navigation tips, tricky elements, etc. -->
