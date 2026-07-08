# CHANGELOG

## [Unreleased]
- **성능 개선**: `i18n.js`에서 초기 로드 시 기본 언어가 한국어(ko)인 경우 불필요한 DOM 순회 및 텍스트 업데이트를 생략하도록 개선했습니다.
- **테스트 추가**: 다국어 처리 로직의 무결성을 검증하기 위해 `test_i18n.html` 테스트 파일을 추가했습니다.

### Security
- **보안 강화**: `index.html`의 CSP에 Trusted Types 지시어(`require-trusted-types-for 'script'`)를 추가하여, 향후 위험한 DOM sink 도입 시에도 문자열 할당을 원천 차단하도록 했습니다.
