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
## 2026-06-29 - Secure External Links with noopener noreferrer
**Vulnerability:** External links (`<a href="http...">`) opened without `rel="noopener noreferrer"`.
**Learning:** While the site didn't previously open links in a new tab (`target="_blank"`), adding this behavior along with `rel="noopener noreferrer"` enhances security by preventing newly opened untrusted tabs from accessing the `window.opener` object to execute reverse tabnabbing attacks.
**Prevention:** Always add `target="_blank" rel="noopener noreferrer"` to external outgoing links to protect users from malicious redirects by third parties.
