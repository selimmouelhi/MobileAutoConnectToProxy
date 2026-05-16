/**
 * Device capabilities configuration
 * Define all device configurations here
 */

const devices = {
  // iOS Simulators
  iphone17ProMax: {
    type: 'simulator',
    platformName: 'iOS',
    'appium:automationName': 'XCUITest',
    'appium:deviceName': 'iPhone 17 Pro Max',
    'appium:platformVersion': '26.0',
    'appium:udid': 'FD7C78EE-530E-4637-8BC0-F1A910C14477',
    'appium:noReset': true,
    'appium:newCommandTimeout': 300,
  },

  iphone15Pro: {
    type: 'simulator',
    platformName: 'iOS',
    'appium:automationName': 'XCUITest',
    'appium:deviceName': 'iPhone 15 Pro',
    'appium:platformVersion': '17.2',
    'appium:udid': 'B72B4EC3-1F6E-42A8-9AAA-A18C54764C1E',
    'appium:noReset': true,
    'appium:newCommandTimeout': 300,
  },

  // Physical device — Selim's iPhone
  selimIphone: {
    type: 'physical',
    platformName: 'iOS',
    'appium:automationName': 'XCUITest',
    'appium:deviceName': "Selim's iPhone",
    'appium:platformVersion': '26.3',
    'appium:udid': '00008140-001C09D608E3C01C',
    'appium:noReset': true,
    'appium:newCommandTimeout': 300,
  },

  // Physical device — I21M-KGC (iPhone 13 Pro)
  i21mKgc: {
    type: 'physical',
    platformName: 'iOS',
    'appium:automationName': 'XCUITest',
    'appium:deviceName': 'I21M-KGC',
    'appium:platformVersion': '26.1',
    'appium:udid': '00008110-001125A13ED8401E',
    'appium:noReset': true,
    'appium:newCommandTimeout': 300,
  },

  // Android Devices
  pixel5: {
    platformName: 'Android',
    'appium:automationName': 'UiAutomator2',
    'appium:deviceName': 'Pixel_5_API_32',
    'appium:avd': 'Pixel_5_API_32',
    'appium:noReset': true,
    'appium:newCommandTimeout': 300,
  },

  xiaomi2201122G: {
    platformName: 'Android',
    'appium:automationName': 'UiAutomator2',
    'appium:deviceName': '2201122G',
    'appium:udid': '460a8e89',
    'appium:noReset': false,
    'appium:fullReset': false,
    'appium:forceAppLaunch': true,
    'appium:newCommandTimeout': 300,
  },

  samsungS22Plus: {
    platformName: 'Android',
    'appium:automationName': 'UiAutomator2',
    'appium:deviceName': 'SM-S906B',
    'appium:udid': 'R3CT500J82D',
    'appium:platformVersion': '14',
    'appium:noReset': true,
    'appium:newCommandTimeout': 300,
  },
};

/**
 * App configurations
 * Define bundle IDs and package names here
 */
const apps = {
  calculator: {
    ios: {
      bundleId: 'com.apple.calculator',
    },
    android: {
      appPackage: 'com.google.android.calculator',
      appActivity: 'com.android.calculator2.Calculator',
    },
  },
  safari: {
    ios: {
      bundleId: 'com.apple.mobilesafari',
    },
  },
  settings: {
    ios: {
      bundleId: 'com.apple.Preferences',
    },
    android: {
      appPackage: 'com.android.settings',
      appActivity: '.Settings',
    },
  },
  imcore: {
    android: {
      appPackage: 'dk.roche.imcore.new_2024',
      appActivity: 'com.roche.imcore.app.MainActivity',
    },
  },
  rema: {
    ios: {
      bundleId: 'dk.rema1000.vigotestflight',
    },
    android: {
      appPackage: 'dk.iroots.rema1000.staging',
      appActivity: 'dk.iroots.rema1000.app.activity.MainActivity',
    },
  },
  remaStaging: {
    android: {
      appPackage: 'dk.iroots.rema1000.staging',
      appActivity: 'dk.iroots.rema1000.app.activity.MainActivity',
    },
  },
};

/**
 * Get capabilities for a specific device and app
 * @param {string} deviceName - Name of the device from devices object
 * @param {string} appName - Name of the app from apps object
 * @returns {object} Combined capabilities
 */
function getCapabilities(deviceName, appName) {
  const device = { ...devices[deviceName] };
  if (!device || !devices[deviceName]) {
    throw new Error(`Device "${deviceName}" not found in capabilities`);
  }

  const app = apps[appName];
  if (!app) {
    throw new Error(`App "${appName}" not found in capabilities`);
  }

  const isPhysical = device.type === 'physical';
  delete device.type;

  const platform = device.platformName.toLowerCase();
  const appConfig = app[platform];

  if (!appConfig) {
    throw new Error(`App "${appName}" not configured for platform "${platform}"`);
  }

  const caps = {
    ...device,
    ...(platform === 'ios'
      ? { 'appium:bundleId': appConfig.bundleId }
      : {
          'appium:appPackage': appConfig.appPackage,
          'appium:appActivity': appConfig.appActivity,
        }
    ),
  };

  // Auto-inject Xcode signing for physical iOS devices
  if (platform === 'ios' && isPhysical) {
    const orgId = process.env.XCODE_ORG_ID;
    const signingId = process.env.XCODE_SIGNING_ID || 'Apple Development';
    if (!orgId) {
      throw new Error('XCODE_ORG_ID is required for physical iOS devices. Set it in .env');
    }
    caps['appium:xcodeOrgId'] = orgId;
    caps['appium:xcodeSigningId'] = signingId;
  }

  return caps;
}

module.exports = {
  devices,
  apps,
  getCapabilities,
};
