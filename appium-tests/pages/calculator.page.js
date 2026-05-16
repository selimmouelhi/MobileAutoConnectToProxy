/**
 * Calculator Page Object
 * Encapsulates all calculator interactions
 */

const { tap, getText, isDisplayed, pause } = require('../helpers');
const { getSelector, getNumberSelector } = require('../selectors');

class CalculatorPage {
  constructor(platform = 'ios') {
    this.platform = platform.toLowerCase();
  }

  // ==================== SELECTORS ====================

  get selectors() {
    return {
      // Numbers
      seven: getNumberSelector(this.platform, 7),

      // Operators
      add: getSelector(this.platform, 'operators', 'add'),
      subtract: getSelector(this.platform, 'operators', 'subtract'),
      multiply: getSelector(this.platform, 'operators', 'multiply'),
      divide: getSelector(this.platform, 'operators', 'divide'),
      equals: getSelector(this.platform, 'operators', 'equals'),

      // Controls
      clear: getSelector(this.platform, 'controls', this.platform === 'ios' ? 'clearOrAllClear' : 'clear'),

      // Display
      result: getSelector(this.platform, 'display', 'result'),
    };
  }

  // ==================== ACTIONS ====================

  /**
   * Tap a number button (0-9)
   * @param {number|string} number - Number to tap
   */
  async tapNumber(number) {
    const selector = getNumberSelector(this.platform, number);
    await tap(selector);
    await pause(200);
  }

  /**
   * Tap multiple numbers in sequence
   * @param {string|number} numbers - Numbers to tap (e.g., "123" or 123)
   */
  async tapNumbers(numbers) {
    const digits = String(numbers).split('');
    for (const digit of digits) {
      await this.tapNumber(digit);
    }
  }

  /**
   * Tap the add (+) button
   */
  async tapAdd() {
    await tap(this.selectors.add);
    await pause(200);
  }

  /**
   * Tap the subtract (-) button
   */
  async tapSubtract() {
    await tap(this.selectors.subtract);
    await pause(200);
  }

  /**
   * Tap the multiply (×) button
   */
  async tapMultiply() {
    await tap(this.selectors.multiply);
    await pause(200);
  }

  /**
   * Tap the divide (÷) button
   */
  async tapDivide() {
    await tap(this.selectors.divide);
    await pause(200);
  }

  /**
   * Tap the equals (=) button
   */
  async tapEquals() {
    await tap(this.selectors.equals);
    await pause(500);
  }

  /**
   * Clear the calculator
   */
  async clear() {
    const isClearVisible = await isDisplayed(this.selectors.clear, 3000);
    if (isClearVisible) {
      await tap(this.selectors.clear);
      await pause(200);
    }
  }

  /**
   * Get the current display result
   * @returns {Promise<string>} Current display value
   */
  async getResult() {
    return getText(this.selectors.result);
  }

  // ==================== COMPOUND ACTIONS ====================

  /**
   * Perform addition: a + b
   * @param {number} a - First number
   * @param {number} b - Second number
   * @returns {Promise<string>} Result
   */
  async add(a, b) {
    await this.clear();
    await this.tapNumbers(a);
    await this.tapAdd();
    await this.tapNumbers(b);
    await this.tapEquals();
    return this.getResult();
  }

  /**
   * Perform subtraction: a - b
   * @param {number} a - First number
   * @param {number} b - Second number
   * @returns {Promise<string>} Result
   */
  async subtract(a, b) {
    await this.clear();
    await this.tapNumbers(a);
    await this.tapSubtract();
    await this.tapNumbers(b);
    await this.tapEquals();
    return this.getResult();
  }

  /**
   * Perform multiplication: a × b
   * @param {number} a - First number
   * @param {number} b - Second number
   * @returns {Promise<string>} Result
   */
  async multiply(a, b) {
    await this.clear();
    await this.tapNumbers(a);
    await this.tapMultiply();
    await this.tapNumbers(b);
    await this.tapEquals();
    return this.getResult();
  }

  /**
   * Perform division: a ÷ b
   * @param {number} a - First number
   * @param {number} b - Second number
   * @returns {Promise<string>} Result
   */
  async divide(a, b) {
    await this.clear();
    await this.tapNumbers(a);
    await this.tapDivide();
    await this.tapNumbers(b);
    await this.tapEquals();
    return this.getResult();
  }
}

module.exports = CalculatorPage;
