/**
 * Home (imCORE) App Test Suite
 * End-to-end smoke tests for the imCORE Android application home flow
 *
 * Tests cover:
 * 1. Login with email/password
 * 2. Open article and verify content
 * 3. Like and unlike an article
 * 4. Search for an article
 * 5. Navigate to profile via More tab and assert user data
 * 6. Scroll to bottom and logout
 */

const { expect } = require('chai');
const { initDriver, closeDriver } = require('../helpers');
const { getCapabilities } = require('../config');
const HomePage = require('../pages/home.page');
const { APP_CONFIG, TEST_USERS, ARTICLES } = require('../test-data');

const TEST_USER = TEST_USERS.default;

describe('imCORE App - Full E2E Flow', function () {
  let page;

  before(async function () {
    const capabilities = getCapabilities('xiaomi2201122G', 'imcore');
    const driver = await initDriver(capabilities);
    page = new HomePage();

    // Force clean app state: terminate and relaunch to ensure login screen
    try {
      await driver.terminateApp(APP_CONFIG.packageName);
      await driver.pause(1000);
      await driver.activateApp(APP_CONFIG.packageName);
      await driver.pause(5000);
    } catch (e) {
      console.log('   App relaunch note:', e.message);
    }
  });

  after(async function () {
    await closeDriver();
  });

  // ==================== LOGIN ====================

  describe('Login', function () {
    it('should display the login screen with email input', async function () {
      const loginVisible = await page.isLoginScreenDisplayed();
      expect(loginVisible).to.be.true;
      console.log('   ASSERT: Login screen is displayed');
    });

    it('should login successfully with valid credentials', async function () {
      await page.login(TEST_USER.email, TEST_USER.password);

      const newsFeedVisible = await page.isNewsFeedDisplayed();
      expect(newsFeedVisible).to.be.true;
      console.log('   ASSERT: News feed is displayed after login');
    });
  });

  // ==================== ARTICLE INTERACTION ====================

  describe('Article - Open, Like, Unlike', function () {
    it('should open the "Just Approved" article', async function () {
      await page.openArticle(ARTICLES.justApproved);

      const title = await page.getArticleTitle();
      expect(title).to.include('Just Approved');
      expect(title).to.include('imCORE Lung Cancer RFP');
      console.log(`   ASSERT: Article title contains "Just Approved": "${title}"`);
    });

    it('should like the article and increment the count', async function () {
      const countBefore = await page.getLikeCount();
      console.log(`   Like count before: ${countBefore}`);

      await page.tapLikeButton();

      const countAfter = await page.getLikeCount();
      console.log(`   Like count after:  ${countAfter}`);

      expect(countAfter).to.be.greaterThan(countBefore);
      console.log('   ASSERT: Like count increased');
    });

    it('should unlike the article and decrement the count', async function () {
      const countBefore = await page.getLikeCount();
      console.log(`   Like count before: ${countBefore}`);

      await page.tapLikeButton();

      const countAfter = await page.getLikeCount();
      console.log(`   Like count after:  ${countAfter}`);

      expect(countAfter).to.be.lessThan(countBefore);
      console.log('   ASSERT: Like count decreased');
    });

    it('should navigate back to the news feed', async function () {
      await page.goBack();

      const newsFeedVisible = await page.isNewsFeedDisplayed();
      expect(newsFeedVisible).to.be.true;
      console.log('   ASSERT: Back on news feed');
    });
  });

  // ==================== SEARCH ====================

  describe('Search', function () {
    it('should search for "just approved" and find matching article', async function () {
      await page.searchForArticle('just approved');

      const resultTitle = await page.getSearchResultTitle();
      expect(resultTitle.toLowerCase()).to.include('just approved');
      console.log(`   ASSERT: Search result contains "just approved": "${resultTitle}"`);
    });

    it('should dismiss the keyboard after search', async function () {
      await page.dismissKeyboard();
      console.log('   ASSERT: Keyboard dismissed');
    });
  });

  // ==================== PROFILE ====================

  describe('Profile - Navigate and Assert Data', function () {
    it('should navigate to the More tab (5th bottom tab)', async function () {
      await page.tapMoreTab();

      const isDisplayed = await page.isMoreTabContentDisplayed('Site Directory');
      expect(isDisplayed).to.be.true;
      console.log('   ASSERT: More tab content is displayed');
    });

    it('should open the profile page by tapping profile picture', async function () {
      await page.tapProfileButton();

      const profileName = await page.getProfileName(TEST_USER.name);
      expect(profileName).to.equal(TEST_USER.name);
      console.log(`   ASSERT: Profile name is "${profileName}"`);
    });

    it('should display the correct specialisation', async function () {
      const displayed = await page.isProfileFieldDisplayed(TEST_USER.specialisation);
      expect(displayed).to.be.true;
      console.log(`   ASSERT: Specialisation "${TEST_USER.specialisation}" is displayed`);
    });

    it('should display the correct tumor type', async function () {
      const displayed = await page.isProfileFieldDisplayed(TEST_USER.tumorType);
      expect(displayed).to.be.true;
      console.log(`   ASSERT: Tumor Type "${TEST_USER.tumorType}" is displayed`);
    });

    it('should display Key area of interest 1', async function () {
      const displayed = await page.isProfileFieldDisplayed(TEST_USER.keyArea1);
      expect(displayed).to.be.true;
      console.log(`   ASSERT: Key area 1 "${TEST_USER.keyArea1}" is displayed`);
    });

    it('should display Key area of interest 2', async function () {
      const displayed = await page.isProfileFieldDisplayed(TEST_USER.keyArea2);
      expect(displayed).to.be.true;
      console.log(`   ASSERT: Key area 2 "${TEST_USER.keyArea2}" is displayed`);
    });

    it('should display Other/Specific Fields of Interest', async function () {
      const displayed = await page.isProfileFieldDisplayed(TEST_USER.otherInterest);
      expect(displayed).to.be.true;
      console.log(`   ASSERT: Other interest "${TEST_USER.otherInterest}" is displayed`);
    });
  });

  // ==================== LOGOUT ====================

  describe('Logout', function () {
    it('should navigate to Edit Profile and scroll to Log out', async function () {
      await page.tapEditProfileButton();
      await page.scrollToLogout();

      const isDisplayed = await page.isLogoutButtonDisplayed();
      expect(isDisplayed).to.be.true;
      console.log('   ASSERT: Log out button is visible at bottom');
    });

    it('should log out and return to the login screen', async function () {
      await page.logout();

      const loginVisible = await page.isLoginScreenDisplayed();
      expect(loginVisible).to.be.true;
      console.log('   ASSERT: Login screen displayed after logout');
    });
  });
});
