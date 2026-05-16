/**
 * Home (imCORE) Page Object
 * Encapsulates all interactions with the imCORE Android app home flow
 */

const { getDriver } = require('../helpers/driver.helper');
const { getHomeSelector, getHomeDynamicSelector, getHomeContainsSelector } = require('../selectors');
const { scrollDown, scrollToText, findClickableNear } = require('../helpers');

class HomePage {
  constructor(platform = 'android') {
    this.platform = platform.toLowerCase();
  }

  // ==================== SELECTORS ====================

  getSelector(category, element) {
    return getHomeSelector(category, element);
  }

  // ==================== HELPERS ====================

  async waitForAppReady() {
    await getDriver().pause(3000);
    await this.dismissNativeDialogs();
  }

  async dismissNativeDialogs() {
    const driver = getDriver();
    await driver.setTimeout({ implicit: 2000 });

    const dialogSelectors = [
      this.getSelector('dialogs', 'allowText'),
      this.getSelector('dialogs', 'allowUpperText'),
      this.getSelector('dialogs', 'whileUsingApp'),
      this.getSelector('dialogs', 'allowButton'),
      this.getSelector('dialogs', 'allowForegroundButton'),
    ];

    for (const selector of dialogSelectors) {
      try {
        const btn = await driver.$(selector);
        if (await btn.isDisplayed()) {
          await btn.click();
          await driver.pause(1000);
        }
      } catch {
        // No dialog found, continue
      }
    }

    await driver.setTimeout({ implicit: 10000 });
  }

  // ==================== ACTIONS ====================

  async login(email, password) {
    await this.waitForAppReady();

    const emailField = await getDriver().$(this.getSelector('login', 'emailField'));
    await emailField.waitForDisplayed({ timeout: 15000 });
    await emailField.setValue(email);

    const continueBtn = await getDriver().$(this.getSelector('login', 'continueButton'));
    await continueBtn.waitForDisplayed({ timeout: 5000 });
    await continueBtn.click();
    await getDriver().pause(3000);

    const passwordField = await getDriver().$(this.getSelector('login', 'passwordField'));
    await passwordField.waitForDisplayed({ timeout: 10000 });
    await passwordField.setValue(password);

    const loginBtn = await getDriver().$(this.getSelector('login', 'loginButton'));
    await loginBtn.click();
    await getDriver().pause(5000);
  }

  async isNewsFeedDisplayed() {
    try {
      const newsTab = await getDriver().$(this.getSelector('tabs', 'news'));
      await newsTab.waitForDisplayed({ timeout: 10000 });
      return true;
    } catch {
      return false;
    }
  }

  async openArticle(titleSubstring) {
    const article = await getDriver().$(getHomeContainsSelector(titleSubstring));
    await article.waitForDisplayed({ timeout: 10000 });
    await article.click();
    await getDriver().pause(3000);
  }

  async getArticleTitle() {
    const titles = await getDriver().$$(this.getSelector('article', 'textViews'));
    for (const title of titles) {
      const text = await title.getText();
      if (text && text.length > 20) {
        return text;
      }
    }
    return '';
  }

  async tapLikeButton() {
    const driver = getDriver();
    const elements = await driver.$$(this.getSelector('article', 'clickableViews'));
    for (const el of elements) {
      const size = await el.getSize();
      const loc = await el.getLocation();
      if (size.width < 200 && size.height < 200 && loc.y > 1000 && loc.y < 1400) {
        await el.click();
        await driver.pause(1500);
        return;
      }
    }
    throw new Error('Like button not found');
  }

  async getLikeCount() {
    const elements = await getDriver().$$(this.getSelector('article', 'textViews'));
    for (const el of elements) {
      const text = await el.getText();
      if (text) {
        const match = text.match(/^\+?(\d{1,2})$/);
        if (match) {
          const location = await el.getLocation();
          if (location.y >= 1050 && location.y <= 1400) {
            return parseInt(match[1], 10);
          }
        }
      }
    }
    return 0;
  }

  async goBack() {
    const driver = getDriver();
    const buttons = await driver.$$(this.getSelector('navigation', 'backButton'));
    if (buttons.length > 0) {
      await buttons[0].click();
    } else {
      await driver.pressKeyCode(4);
    }
    await driver.pause(2000);
  }

  async searchForArticle(query) {
    await this.tapNewsTab();

    const searchField = await getDriver().$(this.getSelector('search', 'editText'));
    await searchField.waitForDisplayed({ timeout: 10000 });
    await searchField.click();
    await searchField.setValue(query);
    await getDriver().pause(2000);
  }

  async getSearchResultTitle() {
    const titles = await getDriver().$$(this.getSelector('article', 'textViews'));
    for (const title of titles) {
      const text = await title.getText();
      if (text && text.length > 20 && text !== 'News') {
        return text;
      }
    }
    return '';
  }

  async dismissKeyboard() {
    await getDriver().pressKeyCode(4);
    await getDriver().pause(500);
  }

  async tapMoreTab() {
    const moreTab = await getDriver().$(this.getSelector('tabs', 'more'));
    await moreTab.waitForDisplayed({ timeout: 10000 });
    await moreTab.click();
    await getDriver().pause(2000);
  }

  async tapNewsTab() {
    const newsTab = await getDriver().$(this.getSelector('tabs', 'news'));
    await newsTab.waitForDisplayed({ timeout: 10000 });
    await newsTab.click();
    await getDriver().pause(2000);
  }

  async tapProfileButton() {
    const driver = getDriver();
    const elements = await driver.$$(this.getSelector('navigation', 'profileButtonArea'));
    for (const el of elements) {
      const loc = await el.getLocation();
      if (loc.x > 800 && loc.y < 250) {
        await el.click();
        await driver.pause(2000);
        return;
      }
    }
    throw new Error('Profile button not found');
  }

  async getProfileName(name) {
    try {
      const el = await getDriver().$(getHomeDynamicSelector(name));
      await el.waitForDisplayed({ timeout: 10000 });
      return await el.getText();
    } catch {
      return '';
    }
  }

  async isProfileFieldDisplayed(fieldValue) {
    try {
      const el = await getDriver().$(getHomeDynamicSelector(fieldValue));
      return await el.isDisplayed();
    } catch {
      return false;
    }
  }

  async tapEditProfileButton() {
    const buttons = await getDriver().$$(this.getSelector('profile', 'editProfileButton'));
    if (buttons.length >= 2) {
      await buttons[1].click();
    } else {
      await buttons[0].click();
    }
    await getDriver().pause(2000);
  }

  async scrollDown() {
    await scrollDown();
  }

  async scrollToLogout() {
    await scrollToText('Log out');
  }

  async logout() {
    const logoutBtn = await getDriver().$(getHomeDynamicSelector('Log out'));
    await logoutBtn.waitForDisplayed({ timeout: 10000 });
    await logoutBtn.click();
    await getDriver().pause(3000);
  }

  async isLoginScreenDisplayed() {
    try {
      await this.dismissNativeDialogs();
      const continueBtn = await getDriver().$(this.getSelector('login', 'continueButton'));
      await continueBtn.waitForDisplayed({ timeout: 15000 });
      return true;
    } catch {
      return false;
    }
  }

  async isMoreTabContentDisplayed(text) {
    try {
      const el = await getDriver().$(getHomeDynamicSelector(text));
      return await el.isDisplayed();
    } catch {
      return false;
    }
  }

  async isLogoutButtonDisplayed() {
    try {
      const el = await getDriver().$(getHomeDynamicSelector('Log out'));
      return await el.isDisplayed();
    } catch {
      return false;
    }
  }
}

module.exports = HomePage;
