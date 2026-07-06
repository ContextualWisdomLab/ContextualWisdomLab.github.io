# CHANGELOG

## [Unreleased]
- **성능 개선**: `styles.css`의 `.section` 클래스에 `content-visibility: auto` 속성을 추가하여 화면 밖 요소의 렌더링을 최적화했습니다.
- **성능 개선**: `i18n.js`에서 초기 로드 시 기본 언어가 한국어(ko)인 경우 불필요한 DOM 순회 및 텍스트 업데이트를 생략하도록 개선했습니다.
- **테스트 추가**: 다국어 처리 로직의 무결성을 검증하기 위해 `test_i18n.html` 테스트 파일을 추가했습니다.
