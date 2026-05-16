# Rema 1000 App — Navigation Map

<!-- AUTO-EXTRACTED -->
<!-- Extracted: 2026-04-01 14:24 -->

## Tab Bar (Bottom Navigation)

The Rema 1000 app has a bottom tab bar with the following tabs:

| Position | Tab Name | Screen | Danish Label |
|----------|----------|--------|-------------|
| 1 | Home | [screens/home.md](screens/home.md) | Hjem |
| 2 | Shopping List | [screens/shopping-list.md](screens/shopping-list.md) | Indkøbsliste |
| 3 | Recipes | [screens/recipes.md](screens/recipes.md) | Opskrifter |
| 4 | Meget mere | [screens/meget-mere.md](screens/meget-mere.md) | Meget mere |
| 5 | Butik | [screens/butik.md](screens/butik.md) | Butik |

## Screen Flow Overview

```
App Launch
├── Cookie Consent (first launch only)
│   └── Accept → Home Screen
├── Home (Hjem tab)
│   ├── Offers / Promotions
│   └── Store info
├── Shopping List (Indkøbsliste tab)
│   ├── Product search → Add to list
│   ├── Recommended Products shelf
│   ├── Pre-Defined Products shelf
│   ├── Share Shopping List → Bottom sheet
│   │   ├── Share Link
│   │   ├── QR Code
│   │   └── Who Has Access
│   └── Checkout (Køb & Hent)
│       ├── Store Selection (GPS suggestions)
│       ├── Payment Method (MobilePay / Worldline)
│       └── Picker Flow
├── Recipes (Opskrifter tab)
│   ├── Search recipes
│   ├── Favorite recipes (heart icon)
│   └── Recipe details → Add to list
└── Meget mere (More tab)
    ├── Profile / Account
    ├── Settings (Indstillinger)
    ├── Help (Zendesk)
    ├── FAQ
    └── Customer Service
```

## Key Entry Points by Feature

- **App Install & Update**: Various
- **Butik (Virtual Store)**: Butik
- **Cookie Consent**: Cookie Consent
- **FAQ Help Page**: Meget mere
- **Faster Picker Flow**: Checkout
- **Favorite Recipes**: Recipes
- **GPS Store Suggestions**: Checkout, Store Selection
- **Home Page**: Home
- **Job Picking**: Checkout
- **Meget Mere**: Meget mere
- **Notifications & Deeplinks**: Various
- **Order Flow**: Checkout
- **Payment Methods**: Checkout
- **Pre-Defined Products**: Shopping List
- **Product Details**: Product Details
- **Recipe Flow**: Recipes
- **Recommended Products**: Shopping List
- **Search & Pre-search**: Search
- **Share Shopping List**: Shopping List
- **Shopping List Interactions**: Shopping List
- **User Login & Signup**: Login / Signup
- **Vigo**: Meget mere, Shopping List
- **Zendesk Help**: Meget mere

<!-- MANUAL -->

## Manual Notes

<!-- Add notes about tricky navigation, login requirements, etc. -->
