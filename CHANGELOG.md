# 변경 이력 (Changelog)

## [Unreleased]
### 성능 개선 (Performance)
- `i18n.js`: 초기 페이지 로딩 시, 기본 언어와 브라우저 언어가 동일할 때 불필요하게 140여 개의 노드를 탐색하는 DOM 쿼리(`querySelectorAll("[data-i18n]")`)를 생략하도록 최적화하여 렌더링 성능을 개선했습니다.
