/**
 * Driver Helper
 * Manages WebDriverIO session lifecycle
 */

const { remote } = require('webdriverio');
const { getWdioConfig } = require('../config');

let driver = null;

/**
 * Initialize WebDriverIO driver
 * @param {object} capabilities - Device and app capabilities
 * @returns {Promise<object>} WebDriverIO driver instance
 */
async function initDriver(capabilities) {
  const config = getWdioConfig(capabilities);

  console.log('🚀 Initializing driver...');
  console.log(`   Device: ${capabilities['appium:deviceName']}`);
  console.log(`   Platform: ${capabilities.platformName} ${capabilities['appium:platformVersion']}`);

  driver = await remote(config);

  // Set implicit wait
  await driver.setTimeout({ implicit: 10000 });

  console.log('   ✅ Driver initialized successfully');
  return driver;
}

/**
 * Get current driver instance
 * @returns {object|null} Current driver or null
 */
function getDriver() {
  return driver;
}

/**
 * Close driver session
 * @returns {Promise<void>}
 */
async function closeDriver() {
  if (driver) {
    console.log('🧹 Closing driver session...');
    await driver.deleteSession();
    driver = null;
    console.log('   ✅ Session closed');
  }
}

/**
 * Check if driver is active
 * @returns {boolean}
 */
function isDriverActive() {
  return driver !== null;
}

/**
 * Restart driver with same or new capabilities
 * @param {object} capabilities - Optional new capabilities
 * @returns {Promise<object>} New driver instance
 */
async function restartDriver(capabilities) {
  await closeDriver();
  return initDriver(capabilities);
}

module.exports = {
  initDriver,
  getDriver,
  closeDriver,
  isDriverActive,
  restartDriver,
};
