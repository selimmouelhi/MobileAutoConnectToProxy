/**
 * Settings App Test Suite
 * Tests for iOS Settings application
 */

const { expect } = require('chai');
const { initDriver, closeDriver, pause } = require('../helpers');
const { getCapabilities } = require('../config');
const SettingsPage = require('../pages/settings.page');

describe('Settings App', function () {
  let settingsPage;

  before(async function () {
    // Setup: Initialize driver and page object
    const capabilities = getCapabilities('iphone17ProMax', 'settings');
    await initDriver(capabilities);
    settingsPage = new SettingsPage('ios');
  });

  after(async function () {
    // Teardown: Close driver session
    await closeDriver();
  });

  // ==================== MAIN SETTINGS PAGE TESTS ====================

  describe('Main Settings Page', function () {
    it('should display the Settings main page', async function () {
      const isDisplayed = await settingsPage.isSettingsPageDisplayed();

      expect(isDisplayed).to.be.true;
      console.log('   ✅ Settings main page is displayed');
    });

    it('should show General option in the menu', async function () {
      const isVisible = await settingsPage.isGeneralVisible();

      expect(isVisible).to.be.true;
      console.log('   ✅ General option is visible');
    });

    it('should show Wi-Fi option in the menu', async function () {
      const isVisible = await settingsPage.isSettingVisible('mainMenu', 'wifi');

      expect(isVisible).to.be.true;
      console.log('   ✅ Wi-Fi option is visible');
    });

    it('should show Bluetooth option in the menu', async function () {
      const isVisible = await settingsPage.isSettingVisible('mainMenu', 'bluetooth');

      expect(isVisible).to.be.true;
      console.log('   ✅ Bluetooth option is visible');
    });
  });

  // ==================== NAVIGATION TESTS ====================

  describe('Navigation', function () {
    it('should navigate to General settings', async function () {
      await settingsPage.goToGeneral();
      await pause(500);

      const isAboutVisible = await settingsPage.isSettingVisible('general', 'about');
      expect(isAboutVisible).to.be.true;
      console.log('   ✅ Successfully navigated to General settings');

      // Go back to main settings
      await settingsPage.goBack();
    });

    it('should navigate to General > About', async function () {
      await settingsPage.goToGeneral();
      await settingsPage.goToAbout();

      const isAboutPageDisplayed = await settingsPage.isAboutPageDisplayed();
      expect(isAboutPageDisplayed).to.be.true;
      console.log('   ✅ Successfully navigated to About page');

      // Go back twice to main settings
      await settingsPage.goBack();
      await settingsPage.goBack();
    });
  });
});
