/**
 * Appium Server Configuration
 */

require('dotenv').config();

const config = {
  // Appium Server
  server: {
    host: process.env.APPIUM_HOST || 'localhost',
    port: parseInt(process.env.APPIUM_PORT, 10) || 4723,
    path: '/',
  },

  // Timeouts (in milliseconds)
  timeouts: {
    implicit: 10000,
    pageLoad: 30000,
    script: 30000,
    newCommand: 300000,
    elementWait: 15000,
  },

  // Retry configuration
  retry: {
    maxAttempts: 3,
    delay: 1000,
  },

  // Logging
  logging: {
    level: process.env.LOG_LEVEL || 'info',
    outputDir: './reports/logs',
  },
};

/**
 * Get WebDriverIO configuration
 * @param {object} capabilities - Device and app capabilities
 * @returns {object} WDIO config object
 */
function getWdioConfig(capabilities) {
  return {
    hostname: config.server.host,
    port: config.server.port,
    path: config.server.path,
    capabilities,
    logLevel: config.logging.level,
    connectionRetryTimeout: config.timeouts.newCommand,
    connectionRetryCount: config.retry.maxAttempts,
  };
}

module.exports = {
  config,
  getWdioConfig,
};
