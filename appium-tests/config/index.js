/**
 * Configuration Index
 * Central export point for all configuration
 */

const { devices, apps, getCapabilities } = require('./capabilities');
const { config, getWdioConfig } = require('./appium.config');

module.exports = {
  // Device and App Capabilities
  devices,
  apps,
  getCapabilities,

  // Appium Configuration
  appiumConfig: config,
  getWdioConfig,

  // Default test configuration
  defaultDevice: 'iphone17ProMax',
  defaultApp: 'calculator',
};
