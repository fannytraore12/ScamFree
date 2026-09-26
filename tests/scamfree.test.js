// tests/scamfree.test.js - automated tests for ScamFree's data loader and classifier.
// Run locally with:  npm test

const natural = require('natural');
const { loadEmails } = require('../CSV_Parser');

const CSV = './123.csv';
jest.setTimeout(300000);
describe('CSV_Parser.loadEmails', () => {
  test('respects the record limit', async () => {
    const emails = await loadEmails(CSV, 10);
    expect(emails.length).toBeLessThanOrEqual(10);
  });

  test('every record has a valid label and text', async () => {
    const emails = await loadEmails(CSV, 200);
    for (const e of emails) {
      expect(['Spam', 'Not Spam']).toContain(e.label);
      expect(typeof e.text).toBe('string');
    }
  });

  test('filters out texts that are too short or too long', async () => {
    const emails = await loadEmails(CSV, 500);
    for (const e of emails) {
      expect(e.text.length).toBeGreaterThanOrEqual(3);
      expect(e.text.length).toBeLessThanOrEqual(2000);
    }
  });

  test('rejects when the file does not exist', async () => {
    await expect(loadEmails('./does-not-exist.csv')).rejects.toBeDefined();
  });
});

describe('Naive Bayes classifier', () => {
  let emails;
  beforeAll(async () => {
    emails = await loadEmails(CSV);
  });

  test('dataset contains both spam and non-spam examples', () => {
    const labels = new Set(emails.map((e) => e.label));
    expect(labels.has('Spam')).toBe(true);
    expect(labels.has('Not Spam')).toBe(true);
  });

  test('only ever predicts a known label', () => {
    const c = new natural.BayesClassifier();
    for (const e of emails.slice(0, 1000)) c.addDocument(e.text, e.label);
    c.train();
    for (const e of emails.slice(1000, 1050)) {
      expect(['Spam', 'Not Spam']).toContain(c.classify(e.text));
    }
  });

  // Quality gate: CI fails if a change drops held-out accuracy below 95%.
  test('held-out accuracy stays at or above 95%', () => {
    const split = Math.floor(emails.length * 0.8);
    const c = new natural.BayesClassifier();
    for (const e of emails.slice(0, split)) c.addDocument(e.text, e.label);
    c.train();
    const test = emails.slice(split);
    const correct = test.filter((e) => c.classify(e.text) === e.label).length;
    expect(correct / test.length).toBeGreaterThanOrEqual(0.95);
  });
});
