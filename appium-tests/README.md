# Appium Test Automation Framework

A professional test automation framework for mobile applications using Appium and WebDriverIO.

## Project Structure

```
appium-tests/
├── config/                    # Configuration files
│   ├── index.js              # Config exports
│   ├── appium.config.js      # Appium server settings
│   └── capabilities.js       # Device & app capabilities
├── helpers/                   # Utility functions
│   ├── index.js              # Helper exports
│   ├── driver.helper.js      # WebDriverIO session management
│   └── element.helper.js     # Element interaction utilities
├── pages/                     # Page Object Models
│   ├── index.js              # Page exports
│   └── calculator.page.js    # Calculator page object
├── selectors/                 # Element selectors
│   ├── index.js              # Selector exports
│   └── calculator.selectors.js # Calculator element selectors
├── tests/                     # Test specifications
│   └── calculator.spec.js    # Calculator test suite
├── reports/                   # Test reports (generated)
├── package.json              # Dependencies & scripts
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## Prerequisites

- Node.js >= 18.0.0
- Appium 2.x installed globally
- Xcode (for iOS testing)
- Android SDK (for Android testing)
- iOS Simulator or Android Emulator

## Installation

```bash
# Navigate to the project directory
cd appium-tests

# Install dependencies
npm install
```

## Configuration

### Device Capabilities

Edit `config/capabilities.js` to add or modify device configurations:

```javascript
const devices = {
  iphone17ProMax: {
    platformName: 'iOS',
    'appium:automationName': 'XCUITest',
    'appium:deviceName': 'iPhone 17 Pro Max',
    'appium:platformVersion': '26.0',
    // ...
  },
};
```

### Environment Variables

Create a `.env` file for environment-specific settings:

```env
APPIUM_HOST=localhost
APPIUM_PORT=4723
LOG_LEVEL=info
```

## Running Tests

### Start Appium Server

```bash
# In a separate terminal
npm run start:appium

# Or manually
appium --relaxed-security --port 4723
```

### Run All Tests

```bash
npm test
```

### Run Calculator Tests

```bash
npm run test:calculator
```

### Run Tests with HTML Report

```bash
npm run test:report
```

Reports will be generated in the `reports/` directory.

## Writing Tests

### Page Object Pattern

Create page objects in `pages/` directory:

```javascript
const { tap, getText } = require('../helpers');

class MyPage {
  get myButton() { return '~buttonId'; }

  async tapMyButton() {
    await tap(this.myButton);
  }
}
```

### Test Structure

Create test files in `tests/` with `.spec.js` extension:

```javascript
const { expect } = require('chai');
const { initDriver, closeDriver } = require('../helpers');

describe('My Feature', function () {
  before(async function () {
    await initDriver(capabilities);
  });

  after(async function () {
    await closeDriver();
  });

  it('should do something', async function () {
    // Test code
  });
});
```

## Selector Strategies

### iOS Selectors

- **Predicate String**: `-ios predicate string:label == "Button"`
- **Class Chain**: `-ios class chain:**/XCUIElementTypeButton`
- **Accessibility ID**: `~accessibilityId`

### Android Selectors

- **Accessibility ID**: `~contentDescription`
- **Resource ID**: `id:package:id/elementId`
- **XPath**: `//android.widget.Button[@text="Click"]`

## Best Practices

1. **Page Object Model**: Encapsulate page interactions in page objects
2. **Reusable Helpers**: Use helper functions for common operations
3. **Descriptive Tests**: Write clear test descriptions
4. **Independent Tests**: Each test should be independent
5. **Clean Up**: Always close sessions in `after` hooks
6. **Meaningful Assertions**: Use specific assertions with clear error messages

## Troubleshooting

### Common Issues

1. **Appium not running**: Ensure Appium server is started
2. **Device not found**: Check device UDID in capabilities
3. **Element not found**: Verify selectors using Appium Inspector
4. **Timeout errors**: Increase timeout values in config

### Debug Mode

Set `LOG_LEVEL=debug` in `.env` for verbose logging.

## Contributing

1. Create a feature branch
2. Write tests for new features
3. Ensure all tests pass
4. Submit a pull request

## License

MIT
