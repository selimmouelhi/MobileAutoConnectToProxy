/**
 * Home (imCORE) App Selectors
 * Organized by category — Android only for now
 */

const homeSelectors = {
  android: {
    dialogs: {
      allowText: '//*[@text="Allow"]',
      allowUpperText: '//*[@text="ALLOW"]',
      whileUsingApp: '//*[@text="While using the app"]',
      allowButton: '//*[@resource-id="com.android.permissioncontroller:id/permission_allow_button"]',
      allowForegroundButton: '//*[@resource-id="com.android.permissioncontroller:id/permission_allow_foreground_only_button"]',
    },

    login: {
      emailField: 'android.widget.EditText',
      continueButton: '//*[@text="Continue"]',
      passwordField: 'android.widget.EditText',
      loginButton: '//*[@text="Login"]',
    },

    tabs: {
      news: '~News',
      more: '~More',
    },

    article: {
      clickableViews: '//android.view.View[@clickable="true"]',
      textViews: 'android.widget.TextView',
    },

    search: {
      editText: 'android.widget.EditText',
    },

    navigation: {
      backButton: 'android.widget.Button',
      profileButtonArea: '//android.view.View[@clickable="true"]',
    },

    profile: {
      editProfileButton: 'android.widget.Button',
    },

    scroll: {
      scrollForward: 'android=new UiScrollable(new UiSelector().scrollable(true)).scrollForward()',
    },
  },
};

/**
 * Get a static selector by category and element name
 * @param {string} category - Category name (dialogs, login, tabs, etc.)
 * @param {string} element - Element name within the category
 * @returns {string} Selector string
 */
function getHomeSelector(category, element) {
  const platformSelectors = homeSelectors.android;

  const categorySelectors = platformSelectors[category];
  if (!categorySelectors) {
    throw new Error(`Category "${category}" not found for home selectors`);
  }

  const selector = categorySelectors[element];
  if (!selector) {
    throw new Error(`Element "${element}" not found in category "${category}"`);
  }

  return selector;
}

/**
 * Build a dynamic selector matching exact text
 * @param {string} text - The exact text to match
 * @returns {string} XPath selector
 */
function getHomeDynamicSelector(text) {
  return `//*[@text="${text}"]`;
}

/**
 * Build a dynamic selector matching partial text
 * @param {string} text - The partial text to match
 * @returns {string} XPath selector
 */
function getHomeContainsSelector(text) {
  return `//*[contains(@text,"${text}")]`;
}

module.exports = {
  homeSelectors,
  getHomeSelector,
  getHomeDynamicSelector,
  getHomeContainsSelector,
};
