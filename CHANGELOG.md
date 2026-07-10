# CHANGELOG

## [Unreleased]
- **성능 최적화**: 애플리케이션 환경이 안전한 `textContent` DOM API만을 사용하여 렌더링되므로, 불필요한 HTML Sanitize 라이브러리(`DOMPurify`) 로딩 스크립트와 `security.js`를 제거하여 빌드/배포 크기를 줄이고 초기 로딩 성능을 개선했습니다.
- **보안 강화**: DOM XSS 공격을 방지하기 위해 CSP에 `require-trusted-types-for 'script'`를 추가했습니다. 현재 애플리케이션은 `textContent`와 같은 안전한 DOM API만 사용하므로 외부 라이브러리 없이 네이티브 보호가 가능합니다.
- **성능 개선**: `i18n.js`에서 초기 로드 시 기본 언어가 한국어(ko)인 경우 불필요한 DOM 순회 및 텍스트 업데이트를 생략하도록 개선했습니다.
- **테스트 추가**: 다국어 처리 로직의 무결성을 검증하기 위해 `test_i18n.html` 테스트 파일을 추가했습니다.
