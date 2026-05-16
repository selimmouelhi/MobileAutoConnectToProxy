/**
 * Helpers Index
 * Central export point for all helpers
 */

const driverHelper = require('./driver.helper');
const elementHelper = require('./element.helper');
const gestureHelper = require('./gesture.helper');

module.exports = {
  // Driver helpers
  initDriver: driverHelper.initDriver,
  getDriver: driverHelper.getDriver,
  closeDriver: driverHelper.closeDriver,
  isDriverActive: driverHelper.isDriverActive,
  restartDriver: driverHelper.restartDriver,

  // Element helpers
  waitForElement: elementHelper.waitForElement,
  tap: elementHelper.tap,
  getText: elementHelper.getText,
  getAttribute: elementHelper.getAttribute,
  isDisplayed: elementHelper.isDisplayed,
  exists: elementHelper.exists,
  sendKeys: elementHelper.sendKeys,
  clearText: elementHelper.clearText,
  waitForText: elementHelper.waitForText,
  takeScreenshot: elementHelper.takeScreenshot,
  pause: elementHelper.pause,

  // Gesture helpers
  scrollDown: gestureHelper.scrollDown,
  scrollToText: gestureHelper.scrollToText,
  findClickableNear: gestureHelper.findClickableNear,
};
