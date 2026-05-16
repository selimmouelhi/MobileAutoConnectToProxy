/**
 * Home (imCORE) Test Data
 * Credentials, user profile fields, and article data
 */

const APP_CONFIG = {
  packageName: 'dk.roche.imcore.new_2024',
};

const TEST_USERS = {
  default: {
    email: 'selim.mouelhi@framna.com',
    password: 'Password1',
    name: 'Selim Mouelhi',
    specialisation: 'Medical/Clinical Oncology/ Hematology',
    tumorType: 'solid',
    keyArea1: 'Brain',
    keyArea2: 'Gyneconcological',
    otherInterest: 'inflamation',
  },
};

const ARTICLES = {
  justApproved: 'Just Approved',
};

module.exports = {
  APP_CONFIG,
  TEST_USERS,
  ARTICLES,
};
