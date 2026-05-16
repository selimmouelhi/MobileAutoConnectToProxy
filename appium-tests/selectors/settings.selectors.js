/**
 * Settings App Selectors
 * Organized by platform and element type
 */

const settingsSelectors = {
  ios: {
    // Main Settings items
    mainMenu: {
      general: '-ios predicate string:label == "General"',
      wifi: '-ios predicate string:label == "Wi-Fi"',
      bluetooth: '-ios predicate string:label == "Bluetooth"',
      notifications: '-ios predicate string:label == "Notifications"',
      sounds: '-ios predicate string:label == "Sounds & Haptics"',
      focus: '-ios predicate string:label == "Focus"',
      screenTime: '-ios predicate string:label == "Screen Time"',
      privacy: '-ios predicate string:label == "Privacy & Security"',
      accessibility: '-ios predicate string:label == "Accessibility"',
      battery: '-ios predicate string:label == "Battery"',
    },

    // General submenu items
    general: {
      about: '-ios predicate string:label == "About"',
      softwareUpdate: '-ios predicate string:label == "Software Update"',
      storage: '-ios predicate string:label CONTAINS "Storage"',
      backgroundAppRefresh: '-ios predicate string:label == "Background App Refresh"',
      dateTime: '-ios predicate string:label == "Date & Time"',
      keyboard: '-ios predicate string:label == "Keyboard"',
      language: '-ios predicate string:label == "Language & Region"',
      reset: '-ios predicate string:label CONTAINS "Reset"',
    },

    // About page items
    about: {
      name: '-ios predicate string:label == "Name"',
      softwareVersion: '-ios predicate string:label == "iOS Version"',
      modelName: '-ios predicate string:label == "Model Name"',
    },

    // Navigation
    navigation: {
      backButton: '-ios predicate string:label == "Settings" AND type == "XCUIElementTypeButton"',
      settingsTitle: '-ios predicate string:label == "Settings" AND type == "XCUIElementTypeStaticText"',
    },

    // Common elements
    common: {
      searchField: '-ios class chain:**/XCUIElementTypeSearchField',
      tableCell: '-ios class chain:**/XCUIElementTypeCell',
    },
  },

  android: {
    // Main Settings items
    mainMenu: {
      wifi: '~Wi-Fi',
      bluetooth: '~Bluetooth',
      network: '~Network & internet',
      display: '~Display',
      sound: '~Sound',
      battery: '~Battery',
      storage: '~Storage',
      security: '~Security',
      about: '~About phone',
    },
  },
};

/**
 * Get selector for a specific element
 * @param {string} platform - 'ios' or 'android'
 * @param {string} category - Category name
 * @param {string} element - Element name
 * @returns {string} Selector string
 */
function getSettingsSelector(platform, category, element) {
  const platformSelectors = settingsSelectors[platform.toLowerCase()];
  if (!platformSelectors) {
    throw new Error(`Platform "${platform}" not supported`);
  }

  const categorySelectors = platformSelectors[category];
  if (!categorySelectors) {
    throw new Error(`Category "${category}" not found for platform "${platform}"`);
  }

  const selector = categorySelectors[element];
  if (!selector) {
    throw new Error(`Element "${element}" not found in category "${category}"`);
  }

  return selector;
}

module.exports = {
  settingsSelectors,
  getSettingsSelector,
};
