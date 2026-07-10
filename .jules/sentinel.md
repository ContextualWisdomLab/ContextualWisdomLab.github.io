## 2026-06-19 - Added Content Security Policy
**Vulnerability:** Missing Content Security Policy (CSP) header.
**Learning:** Static HTML sites often neglect CSP, leaving them exposed to XSS or data injection if they later add dynamic content or if third-party scripts are compromised.
**Prevention:** Always include a strict baseline CSP (`default-src 'self'`) in `index.html` for static sites to establish defense-in-depth from the start.
## 2024-10-24 - Fix prototype pollution risk in i18n language parsing
**Vulnerability:** Unvalidated user input from `location.search` was used directly as an object key (`messages[query]`). This allowed an attacker to supply `?lang=__proto__` or `?lang=valueOf`, resulting in `messages[query]` returning built-in objects or functions rather than the intended language strings.
**Learning:** Checking for truthiness like `messages[query] ? query : ...` fails securely when dealing with inherited Object properties. Without a whitelist, user input accessing un-prototyped object keys is dangerous.
**Prevention:** Always validate external input against a strict whitelist (e.g. `['ko', 'en'].includes(query)`) before using it in application logic, or ensure dictionaries are created without prototypes (`Object.create(null)`).
## 2024-06-21 - Fix SecurityError crash from strict privacy modes
**Vulnerability:** Unhandled exceptions when accessing `localStorage` in strict browser privacy modes (e.g., when cookies are blocked).
**Learning:** Browsers throw a `SecurityError` when `localStorage` is accessed and the user has blocked third-party cookies or is in a strict privacy mode. If unhandled, this crashes the executing script, leading to a degraded user experience (DoS-like behavior for privacy-conscious users).
**Prevention:** Always wrap `localStorage.getItem` and `localStorage.setItem` in `try-catch` blocks to fail securely and fall back to sensible defaults.
## 2026-06-27 - 외부 링크의 reverse tabnabbing 취약점 완화
**Vulnerability:** 외부 링크(특히 참조문헌 링크 등)에 `target="_blank"` 속성을 사용하거나 새 탭으로 여는 동작을 유도할 때, `rel="noopener noreferrer"` 속성이 누락되어 Reverse Tabnabbing 공격에 노출될 수 있음.
**Learning:** `rel="noopener noreferrer"`가 없으면 새로 열린 탭의 페이지가 `window.opener` 객체를 통해 원래 페이지의 `location`을 악의적인 사이트로 변경할 수 있습니다.
**Prevention:** 외부 링크를 새 탭으로 열기 위해 `target="_blank"`를 사용할 때만 `rel="noopener noreferrer"`를 함께 추가하여 부모 창에 대한 접근을 차단해야 합니다.
## 2026-07-01 - Add Trusted Types Policy via DOMPurify
**Vulnerability:** Application lacked Trusted Types enforcement, which left it potentially vulnerable to DOM-based XSS if DOM sinks (like `innerHTML`) were manipulated.
**Learning:** Enforcing `require-trusted-types-for 'script'` in CSP causes Chromium-based browsers to throw a Trusted Types violation (a `TypeError`) when a string is assigned to a DOM sink without a registered policy, rather than crashing the browser.
**Prevention:** When a default Trusted Types policy is needed, pair the CSP `require-trusted-types-for 'script'` directive with a defensively loaded sanitizer such as DOMPurify, defer the scripts in dependency order, and keep policy creation wrapped so an existing policy or CSP restriction does not break page load.
## 2026-07-08 - Trusted Types 기본 방어 적용
**Vulnerability:** DOM 기반 XSS (안전하지 않은 DOM 싱크 노출 위험)
**Learning:** 이 앱은 주로 `textContent`와 같은 안전한 DOM API를 사용하고 `innerHTML` 등의 위험한 싱크를 피함. 이러한 환경에서는 브라우저 네이티브인 `require-trusted-types-for 'script'` CSP 규칙이 1차 방어선이며, 기본 Trusted Types 정책과 DOMPurify는 실제 HTML 싱크 또는 호환성 요구가 있을 때 방어적으로 로드해야 함.
**Prevention:** 새로운 기능을 추가할 때 앱의 DOM API 사용 방식을 먼저 파악하고, 네이티브 Trusted Types CSP만으로 충분한지 또는 DOMPurify 기반 기본 정책이 필요한지 판단할 것. 기본 정책을 유지한다면 `window.trustedTypes`와 `window.DOMPurify`를 확인하고 `try/catch`로 감싸 페이지 로드를 깨지 않도록 할 것.
