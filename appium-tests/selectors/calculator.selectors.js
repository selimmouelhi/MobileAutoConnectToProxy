/**
 * Calculator App Selectors
 * Organized by platform and element type
 */

const calculatorSelectors = {
  ios: {
    // Number buttons
    buttons: {
      zero: '-ios predicate string:label == "0"',
      one: '-ios predicate string:label == "1"',
      two: '-ios predicate string:label == "2"',
      three: '-ios predicate string:label == "3"',
      four: '-ios predicate string:label == "4"',
      five: '-ios predicate string:label == "5"',
      six: '-ios predicate string:label == "6"',
      seven: '-ios predicate string:label == "7"',
      eight: '-ios predicate string:label == "8"',
      nine: '-ios predicate string:label == "9"',
    },

    // Operator buttons
    operators: {
      add: '-ios predicate string:label == "Add"',
      subtract: '-ios predicate string:label == "Subtract"',
      multiply: '-ios predicate string:label == "Multiply"',
      divide: '-ios predicate string:label == "Divide"',
      equals: '-ios predicate string:label == "Equals"',
      decimal: '-ios predicate string:label == "Decimal"',
      percent: '-ios predicate string:label == "Percent"',
      negate: '-ios predicate string:label == "Negate"',
    },

    // Control buttons
    controls: {
      clear: '-ios predicate string:label == "Clear"',
      allClear: '-ios predicate string:label == "All Clear"',
      clearOrAllClear: '-ios predicate string:label == "Clear" OR label == "All Clear"',
    },

    // Display
    display: {
      result: '-ios class chain:**/XCUIElementTypeStaticText',
      mainDisplay: '~Display',
    },
  },

  android: {
    // Number buttons
    buttons: {
      zero: '~0',
      one: '~1',
      two: '~2',
      three: '~3',
      four: '~4',
      five: '~5',
      six: '~6',
      seven: '~7',
      eight: '~8',
      nine: '~9',
    },

    // Operator buttons
    operators: {
      add: '~plus',
      subtract: '~minus',
      multiply: '~multiply',
      divide: '~divide',
      equals: '~equals',
      decimal: '~point',
      percent: '~percent',
    },

    // Control buttons
    controls: {
      clear: '~clear',
      delete: '~delete',
    },

    // Display
    display: {
      result: 'id:com.google.android.calculator:id/result_final',
      formula: 'id:com.google.android.calculator:id/formula',
    },
  },
};

/**
 * Get selector for a specific element
 * @param {string} platform - 'ios' or 'android'
 * @param {string} category - 'buttons', 'operators', 'controls', or 'display'
 * @param {string} element - Element name
 * @returns {string} Selector string
 */
function getSelector(platform, category, element) {
  const platformSelectors = calculatorSelectors[platform.toLowerCase()];
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

/**
 * Get number button selector
 * @param {string} platform - 'ios' or 'android'
 * @param {number|string} number - Number 0-9
 * @returns {string} Selector string
 */
function getNumberSelector(platform, number) {
  const numberNames = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'];
  const name = numberNames[parseInt(number, 10)];
  return getSelector(platform, 'buttons', name);
}

module.exports = {
  calculatorSelectors,
  getSelector,
  getNumberSelector,
};
