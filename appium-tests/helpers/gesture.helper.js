/**
 * Gesture Helpers
 * Shared scroll, swipe, and element-finding utilities
 */

const { getDriver } = require('./driver.helper');

/**
 * Scroll down using UiAutomator scrollForward, with W3C actions fallback
 */
async function scrollDown() {
  const driver = getDriver();
  try {
    await driver.$('android=new UiScrollable(new UiSelector().scrollable(true)).scrollForward()');
  } catch {
    await driver.performActions([
      {
        type: 'pointer',
        id: 'finger1',
        parameters: { pointerType: 'touch' },
        actions: [
          { type: 'pointerMove', duration: 0, x: 540, y: 1600 },
          { type: 'pointerDown', button: 0 },
          { type: 'pause', duration: 200 },
          { type: 'pointerMove', duration: 600, x: 540, y: 400 },
          { type: 'pointerUp', button: 0 },
        ],
      },
    ]);
    await driver.releaseActions();
  }
  await driver.pause(1000);
}

/**
 * Scroll until a given text is visible (UiAutomator scrollTextIntoView with manual fallback)
 * @param {string} text - The text to scroll to
 */
async function scrollToText(text) {
  const driver = getDriver();
  try {
    await driver.$(`android=new UiScrollable(new UiSelector().scrollable(true)).scrollTextIntoView("${text}")`);
    await driver.pause(1000);
  } catch {
    for (let i = 0; i < 5; i++) {
      await scrollDown();
      try {
        const el = await driver.$(`//*[@text="${text}"]`);
        if (await el.isDisplayed()) break;
      } catch {
        // keep scrolling
      }
    }
  }
}

/**
 * Find the first clickable View element near a given y coordinate
 * @param {number} y - Target y coordinate
 * @param {number} [tolerance=150] - Pixel tolerance
 * @returns {Promise<WebdriverIO.Element|null>}
 */
async function findClickableNear(y, tolerance = 150) {
  const elements = await getDriver().$$('//android.view.View[@clickable="true"]');
  for (const el of elements) {
    const loc = await el.getLocation();
    if (Math.abs(loc.y - y) < tolerance) {
      return el;
    }
  }
  return null;
}

module.exports = {
  scrollDown,
  scrollToText,
  findClickableNear,
};
