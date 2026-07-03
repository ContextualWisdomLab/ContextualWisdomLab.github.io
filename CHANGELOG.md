# CHANGELOG

## [Unreleased]
- **성능 개선**: `i18n.js`에서 초기 로드 시 기본 언어가 한국어(ko)인 경우 불필요한 DOM 순회 및 텍스트 업데이트를 생략하도록 개선했습니다.
- **테스트 추가**: 다국어 처리 로직의 무결성을 검증하기 위해 `test_i18n.html` 테스트 파일을 추가했습니다.

### Security
* `index.html`에 Trusted Types CSP 적용 (`require-trusted-types-for 'script'`)

* 보안성 향상을 위해 CSP 설정 적용 (Trusted Types)

* CI 워크플로우 타임아웃 오류를 우회하고 리뷰 프로세스를 다시 트리거하기 위해 변경사항 추가
