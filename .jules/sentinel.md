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
## 2026-07-07 - CSP에 Trusted Types 강제 적용
**Vulnerability:** `require-trusted-types-for 'script'` 지시문이 없으면, 향후 `innerHTML`과 같은 위험한 DOM 싱크가 코드베이스에 도입될 경우 DOM 기반 XSS(크로스 사이트 스크립팅) 취약점에 노출될 수 있습니다.
**Learning:** `textContent`와 같은 안전한 DOM API만을 독점적으로 사용하고 위험한 싱크를 포함하지 않는 애플리케이션은, 외부 정책 객체(policy)나 새니타이저(sanitizer) 없이도 네이티브하게 Trusted Types를 강제할 수 있습니다. 이는 미래의 DOM XSS 도입을 원천 차단하는 강력한 다층 방어(defense-in-depth) 수단을 제공합니다.
**Prevention:** 애플리케이션이 안전한 DOM API만을 사용할 때 CSP에 `require-trusted-types-for 'script'`를 항상 강제하여, 실수로 DOM XSS 취약점이 도입되는 것을 예방해야 합니다.
