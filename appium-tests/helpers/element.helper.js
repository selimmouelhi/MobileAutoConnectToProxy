/**
 * Element Helper
 * Common element interaction utilities
 */

const { getDriver } = require('./driver.helper');
const { appiumConfig } = require('../config');

/**
 * Wait for element to be displayed
 * @param {string} selector - Element selector
 * @param {number} timeout - Timeout in ms (optional)
 * @returns {Promise<object>} Element
 */
async function waitForElement(selector, timeout = appiumConfig.timeouts.elementWait) {
  const driver = getDriver();
  const element = await driver.$(selector);
  await element.waitForDisplayed({ timeout });
  return element;
}

/**
 * Tap on an element
 * @param {string} selector - Element selector
 * @returns {Promise<void>}
 */
async function tap(selector) {
  const element = await waitForElement(selector);
  await element.click();
}

/**
 * Get element text
 * @param {string} selector - Element selector
 * @returns {Promise<string>} Element text
 */
async function getText(selector) {
  const element = await waitForElement(selector);
  return element.getText();
}

/**
 * Get element attribute
 * @param {string} selector - Element selector
 * @param {string} attribute - Attribute name
 * @returns {Promise<string>} Attribute value
 */
async function getAttribute(selector, attribute) {
  const element = await waitForElement(selector);
  return element.getAttribute(attribute);
}

/**
 * Check if element is displayed
 * @param {string} selector - Element selector
 * @param {number} timeout - Timeout in ms (optional)
 * @returns {Promise<boolean>}
 */
async function isDisplayed(selector, timeout = 5000) {
  const driver = getDriver();
  try {
    const element = await driver.$(selector);
    await element.waitForDisplayed({ timeout });
    return true;
  } catch {
    return false;
  }
}

/**
 * Check if element exists
 * @param {string} selector - Element selector
 * @returns {Promise<boolean>}
 */
async function exists(selector) {
  const driver = getDriver();
  const element = await driver.$(selector);
  return element.isExisting();
}

/**
 * Send keys to an element
 * @param {string} selector - Element selector
 * @param {string} text - Text to send
 * @returns {Promise<void>}
 */
async function sendKeys(selector, text) {
  const element = await waitForElement(selector);
  await element.setValue(text);
}

/**
 * Clear element text
 * @param {string} selector - Element selector
 * @returns {Promise<void>}
 */
async function clearText(selector) {
  const element = await waitForElement(selector);
  await element.clearValue();
}

/**
 * Wait for element to contain text
 * @param {string} selector - Element selector
 * @param {string} text - Expected text
 * @param {number} timeout - Timeout in ms
 * @returns {Promise<boolean>}
 */
async function waitForText(selector, text, timeout = appiumConfig.timeouts.elementWait) {
  const driver = getDriver();
  const element = await driver.$(selector);

  try {
    await driver.waitUntil(
      async () => {
        const elementText = await element.getText();
        return elementText.includes(text);
      },
      { timeout, timeoutMsg: `Element did not contain text "${text}" within ${timeout}ms` }
    );
    return true;
  } catch {
    return false;
  }
}

/**
 * Take screenshot
 * @param {string} filename - Screenshot filename (without extension)
 * @returns {Promise<string>} Screenshot path
 */
async function takeScreenshot(filename) {
  const driver = getDriver();
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const path = `./reports/screenshots/${filename}_${timestamp}.png`;
  await driver.saveScreenshot(path);
  return path;
}

/**
 * Pause execution
 * @param {number} ms - Milliseconds to pause
 * @returns {Promise<void>}
 */
async function pause(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

module.exports = {
  waitForElement,
  tap,
  getText,
  getAttribute,
  isDisplayed,
  exists,
  sendKeys,
  clearText,
  waitForText,
  takeScreenshot,
  pause,
};
