# CHANGELOG

## [Unreleased]
- **보안 개선**: `i18n.js`의 `setLanguage()` 함수에 허용된 언어인지 확인하는 입력값 검증(Input Validation) 로직을 추가하여 Prototype Pollution 및 유효하지 않은 상태 주입을 방지했습니다.
- **성능 개선**: `i18n.js`에서 초기 로드 시 기본 언어가 한국어(ko)인 경우 불필요한 DOM 순회 및 텍스트 업데이트를 생략하도록 개선했습니다.
- **테스트 추가**: 다국어 처리 로직의 무결성을 검증하기 위해 `test_i18n.html` 테스트 파일을 추가했습니다.
