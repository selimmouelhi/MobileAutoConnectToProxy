/**
 * Calculator App Test Suite
 * Tests for iOS Calculator application
 */

const { expect } = require('chai');
const { initDriver, closeDriver } = require('../helpers');
const { getCapabilities } = require('../config');
const CalculatorPage = require('../pages/calculator.page');

describe('Calculator App', function () {
  let calculatorPage;

  before(async function () {
    // Setup: Initialize driver and page object
    const capabilities = getCapabilities('iphone17ProMax', 'calculator');
    await initDriver(capabilities);
    calculatorPage = new CalculatorPage('ios');
  });

  after(async function () {
    // Teardown: Close driver session
    await closeDriver();
  });

  beforeEach(async function () {
    // Clear calculator before each test
    await calculatorPage.clear();
  });

  // ==================== ADDITION TESTS ====================

  describe('Addition', function () {
    it('should calculate 7 + 7 = 14', async function () {
      const result = await calculatorPage.add(7, 7);

      console.log(`   Result: ${result}`);
      expect(result).to.include('14');
    });

    it('should calculate 25 + 75 = 100', async function () {
      const result = await calculatorPage.add(25, 75);

      console.log(`   Result: ${result}`);
      expect(result).to.include('100');
    });

    it('should calculate 0 + 0 = 0', async function () {
      const result = await calculatorPage.add(0, 0);

      console.log(`   Result: ${result}`);
      expect(result).to.include('0');
    });
  });

  // ==================== SUBTRACTION TESTS ====================

  describe('Subtraction', function () {
    it('should calculate 15 - 8 = 7', async function () {
      const result = await calculatorPage.subtract(15, 8);

      console.log(`   Result: ${result}`);
      expect(result).to.include('7');
    });

    it('should calculate 100 - 50 = 50', async function () {
      const result = await calculatorPage.subtract(100, 50);

      console.log(`   Result: ${result}`);
      expect(result).to.include('50');
    });
  });

  // ==================== MULTIPLICATION TESTS ====================

  describe('Multiplication', function () {
    it('should calculate 6 × 7 = 42', async function () {
      const result = await calculatorPage.multiply(6, 7);

      console.log(`   Result: ${result}`);
      expect(result).to.include('42');
    });

    it('should calculate 12 × 12 = 144', async function () {
      const result = await calculatorPage.multiply(12, 12);

      console.log(`   Result: ${result}`);
      expect(result).to.include('144');
    });
  });

  // ==================== DIVISION TESTS ====================

  describe('Division', function () {
    it('should calculate 100 ÷ 5 = 20', async function () {
      const result = await calculatorPage.divide(100, 5);

      console.log(`   Result: ${result}`);
      expect(result).to.include('20');
    });

    it('should calculate 81 ÷ 9 = 9', async function () {
      const result = await calculatorPage.divide(81, 9);

      console.log(`   Result: ${result}`);
      expect(result).to.include('9');
    });
  });
});
