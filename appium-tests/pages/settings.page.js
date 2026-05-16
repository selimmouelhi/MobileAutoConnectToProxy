/**
 * Settings Page Object
 * Encapsulates all Settings app interactions
 */

const { tap, getText, isDisplayed, pause, waitForElement } = require('../helpers');
const { getSettingsSelector } = require('../selectors');

class SettingsPage {
  constructor(platform = 'ios') {
    this.platform = platform.toLowerCase();
  }

  // ==================== SELECTORS ====================

  getSelector(category, element) {
    return getSettingsSelector(this.platform, category, element);
  }

  // ==================== NAVIGATION ====================

  /**
   * Navigate to General settings
   */
  async goToGeneral() {
    await tap(this.getSelector('mainMenu', 'general'));
    await pause(500);
  }

  /**
   * Navigate to About page (from General)
   */
  async goToAbout() {
    await tap(this.getSelector('general', 'about'));
    await pause(500);
  }

  /**
   * Navigate to Wi-Fi settings
   */
  async goToWifi() {
    await tap(this.getSelector('mainMenu', 'wifi'));
    await pause(500);
  }

  /**
   * Navigate to Bluetooth settings
   */
  async goToBluetooth() {
    await tap(this.getSelector('mainMenu', 'bluetooth'));
    await pause(500);
  }

  /**
   * Navigate to Accessibility settings
   */
  async goToAccessibility() {
    await tap(this.getSelector('mainMenu', 'accessibility'));
    await pause(500);
  }

  /**
   * Go back to previous screen
   */
  async goBack() {
    await tap(this.getSelector('navigation', 'backButton'));
    await pause(300);
  }

  // ==================== VERIFICATIONS ====================

  /**
   * Check if Settings main page is displayed
   * @returns {Promise<boolean>}
   */
  async isSettingsPageDisplayed() {
    return isDisplayed(this.getSelector('mainMenu', 'general'), 5000);
  }

  /**
   * Check if General menu item is visible
   * @returns {Promise<boolean>}
   */
  async isGeneralVisible() {
    return isDisplayed(this.getSelector('mainMenu', 'general'), 5000);
  }

  /**
   * Check if About page is displayed
   * @returns {Promise<boolean>}
   */
  async isAboutPageDisplayed() {
    return isDisplayed(this.getSelector('about', 'name'), 5000);
  }

  /**
   * Check if a specific setting exists
   * @param {string} category - Selector category
   * @param {string} element - Element name
   * @returns {Promise<boolean>}
   */
  async isSettingVisible(category, element) {
    return isDisplayed(this.getSelector(category, element), 5000);
  }

  // ==================== DATA RETRIEVAL ====================

  /**
   * Get device name from About page
   * @returns {Promise<string>}
   */
  async getDeviceName() {
    await this.goToGeneral();
    await this.goToAbout();
    const nameElement = await waitForElement(this.getSelector('about', 'name'));
    return nameElement.getText();
  }
}

module.exports = SettingsPage;
