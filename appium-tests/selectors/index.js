/**
 * Selectors Index
 * Central export point for all selectors
 */

const { calculatorSelectors, getSelector, getNumberSelector } = require('./calculator.selectors');
const { settingsSelectors, getSettingsSelector } = require('./settings.selectors');
const { homeSelectors, getHomeSelector, getHomeDynamicSelector, getHomeContainsSelector } = require('./home.selectors');

module.exports = {
  calculatorSelectors,
  getSelector,
  getNumberSelector,
  settingsSelectors,
  getSettingsSelector,
  homeSelectors,
  getHomeSelector,
  getHomeDynamicSelector,
  getHomeContainsSelector,
};
