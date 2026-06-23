// A simple test runner since there's no package manager
const assert = require('assert');

// Mock DOM
global.document = {
  documentElement: { lang: 'ko' },
  title: '맥락지혜 연구실 | Contextual Wisdom Lab',
  querySelector: () => null,
  querySelectorAll: () => []
};

global.window = {
  location: { search: '' }
};

global.navigator = { language: 'ko' };
global.localStorage = { getItem: () => null, setItem: () => {} };

// Try loading script (this will fail because of DOM dependencies like element manipulation)
