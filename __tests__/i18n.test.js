/**
 * @jest-environment jsdom
 */

describe('i18n.js tests', () => {
  beforeEach(() => {
    document.documentElement.lang = 'ko';
    document.title = '맥락지혜 연구실 | Contextual Wisdom Lab';
    document.head.innerHTML = `
      <meta name="description" content="맥락지혜 연구실은 흩어진 기업 자료를 맥락 안에서 판단 가능한 구조로 바꾸는 AI 의사결정 지원 시스템을 연구하고 만듭니다.">
      <meta property="og:description" content="맥락지혜 연구실은 흩어진 기업 자료를 맥락 안에서 판단 가능한 구조로 바꾸는 AI 의사결정 지원 시스템을 연구하고 만듭니다.">
    `;
    document.body.innerHTML = `
      <div class="language-switch" role="group" aria-label="Language">
        <button type="button" data-lang="ko" aria-pressed="true">KO</button>
        <button type="button" data-lang="en" aria-pressed="false">EN</button>
      </div>
      <h1 data-i18n="hero.title">맥락지혜 연구실</h1>
      <img id="footer-logo" src="assets/context-wisdom-lab-logo.svg" alt="맥락지혜 연구실 · Contextual Wisdom Lab">
    `;

    Object.defineProperty(window, 'localStorage', {
      value: {
        getItem: jest.fn(),
        setItem: jest.fn(),
        clear: jest.fn()
      },
      writable: true
    });

    jest.resetModules();
  });

  it('should cover existing document lang and attributes already matching the dictionary', () => {
    Object.defineProperty(window.navigator, 'language', { value: 'ko-KR', configurable: true });
    require('../i18n.js');

    const enButton = document.querySelector('button[data-lang="en"]');
    enButton.click();

    // Manually force ALL properties to match 'ko' EXCEPT we leave the state in EN
    // so when we click 'ko' it evaluates the updates but skips because they match.
    document.documentElement.lang = 'ko'; // Cover line 326 `document.documentElement.lang !== lang`
    document.title = '맥락지혜 연구실 | Contextual Wisdom Lab';
    document.querySelector('meta[name="description"]').setAttribute('content', '맥락지혜 연구실은 흩어진 기업 자료를 맥락 안에서 판단 가능한 구조로 바꾸는 AI 의사결정 지원 시스템을 연구하고 만듭니다.');
    document.querySelector('meta[property="og:description"]').setAttribute('content', '맥락지혜 연구실은 흩어진 기업 자료를 맥락 안에서 판단 가능한 구조로 바꾸는 AI 의사결정 지원 시스템을 연구하고 만듭니다.');
    document.querySelector('#footer-logo').setAttribute('src', 'assets/context-wisdom-lab-logo.svg');
    document.querySelector('#footer-logo').setAttribute('alt', '맥락지혜 연구실 · Contextual Wisdom Lab');

    const koButton = document.querySelector('button[data-lang="ko"]');
    koButton.click();
  });

  it('should initialize without updating DOM when lang matches', () => {
    Object.defineProperty(window.navigator, 'language', { value: 'ko-KR', configurable: true });
    require('../i18n.js');
    expect(document.documentElement.lang).toBe('ko');
  });

  it('should update DOM when lang does not match', () => {
    Object.defineProperty(window.navigator, 'language', { value: 'en-US', configurable: true });
    require('../i18n.js');
    expect(document.documentElement.lang).toBe('en');
    expect(document.title).toBe('Contextual Wisdom Lab');
  });

  it('should switch language on button click', () => {
    Object.defineProperty(window.navigator, 'language', { value: 'ko-KR', configurable: true });
    require('../i18n.js');
    const enButton = document.querySelector('button[data-lang="en"]');
    enButton.click();
    expect(document.documentElement.lang).toBe('en');
  });

  it('should not update DOM if switching to same language', () => {
    Object.defineProperty(window.navigator, 'language', { value: 'ko-KR', configurable: true });
    require('../i18n.js');
    const koButton = document.querySelector('button[data-lang="ko"]');
    koButton.click();
    expect(document.documentElement.lang).toBe('ko');
  });

  it('should read from URL query if available', () => {
    delete window.location;
    window.location = new URL('http://localhost/?lang=en');
    Object.defineProperty(window.navigator, 'language', { value: 'ko-KR', configurable: true });
    require('../i18n.js');
    expect(document.documentElement.lang).toBe('en');
  });

  it('should fallback if URL query is invalid', () => {
    delete window.location;
    window.location = new URL('http://localhost/?lang=fr');
    Object.defineProperty(window.navigator, 'language', { value: 'ko-KR', configurable: true });
    require('../i18n.js');
    expect(document.documentElement.lang).toBe('ko');
  });

  it('should read from localStorage if available', () => {
    window.localStorage.getItem.mockReturnValue('en');
    Object.defineProperty(window.navigator, 'language', { value: 'ko-KR', configurable: true });
    require('../i18n.js');
    expect(document.documentElement.lang).toBe('en');
  });

  it('should fallback if localStorage is invalid', () => {
    window.localStorage.getItem.mockReturnValue('fr');
    Object.defineProperty(window.navigator, 'language', { value: 'ko-KR', configurable: true });
    require('../i18n.js');
    expect(document.documentElement.lang).toBe('ko');
  });

  it('should fallback to navigator.language when query and localStorage are absent', () => {
    window.localStorage.getItem.mockReturnValue(null);
    Object.defineProperty(window.navigator, 'language', { value: 'en-US', configurable: true });
    require('../i18n.js');
    expect(document.documentElement.lang).toBe('en');
  });

  it('should default to en if navigator.language is missing', () => {
    window.localStorage.getItem.mockReturnValue(null);
    Object.defineProperty(window.navigator, 'language', { value: undefined, configurable: true });
    require('../i18n.js');
    expect(document.documentElement.lang).toBe('en');
  });

  it('should handle localStorage throw error securely', () => {
    window.localStorage.getItem.mockImplementation(() => { throw new Error('Strict mode error'); });
    Object.defineProperty(window.navigator, 'language', { value: 'en-US', configurable: true });
    require('../i18n.js');
    expect(document.documentElement.lang).toBe('en');
  });

  it('should handle localStorage setItem throw error securely', () => {
    window.localStorage.setItem.mockImplementation(() => { throw new Error('Strict mode error'); });
    Object.defineProperty(window.navigator, 'language', { value: 'en-US', configurable: true });
    expect(() => {
      require('../i18n.js');
    }).not.toThrow();
  });

  it('should cover missing DOM elements gracefully', () => {
    document.head.innerHTML = '';
    document.body.innerHTML = `
      <button type="button" data-lang="en" aria-pressed="false">EN</button>
      <h1 data-i18n="hero.title">맥락지혜 연구실</h1>
    `;
    Object.defineProperty(window.navigator, 'language', { value: 'en-US', configurable: true });
    require('../i18n.js');
    expect(document.documentElement.lang).toBe('en');
  });

  it('should cover fallback language in dict and edge case where attributes match', () => {
    document.body.innerHTML = `
      <button type="button" data-lang="fr" aria-pressed="false">FR</button>
      <button type="button" data-lang="ko" aria-pressed="false">KO</button>
      <h1 data-i18n="invalid.key">Not changing</h1>
    `;
    Object.defineProperty(window.navigator, 'language', { value: 'en-US', configurable: true });
    require('../i18n.js');
    const frButton = document.querySelector('button[data-lang="fr"]');
    frButton.click();
  });
});
