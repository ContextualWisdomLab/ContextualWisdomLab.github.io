# CHANGELOG

## [Unreleased]
- **보안 개선**: 컴포넌트 갤러리의 인라인 스크립트와 스타일을 외부 파일로 분리하고, 엄격한 Content-Security-Policy를 적용해 XSS 방어를 강화했습니다.
- **성능 회귀 복원**: 오프스크린 `.section` 렌더링을 `content-visibility: auto`로 지연하고, 일반 섹션은 600px·콘텐츠가 큰 DIKW/projects 섹션은 1000px의 `contain-intrinsic-size` placeholder를 유지해 초기 렌더링 비용과 스크롤바 이동을 함께 줄였습니다.
- **보안 개선**: Trusted Types 기반 CSP 강화: 잠재적인 DOM 기반 XSS 공격을 방지하기 위해 `require-trusted-types-for 'script'` 지시어 추가
- **UX/접근성 개선**: `.dikw-grid span`의 텍스트 색상을 `var(--gold)`에서 `var(--teal)`로 변경하여 밝은 배경에서의 대비(Color Contrast)를 개선하고 WCAG 접근성 기준을 충족하도록 하였습니다.
- **UX/접근성 개선**: 시스템 설정에서 '애니메이션 줄이기(prefers-reduced-motion)'를 활성화한 사용자를 위해 과도한 애니메이션과 트랜지션을 비활성화(`0.01ms`)하고 부드러운 스크롤을 끄도록 CSS 미디어 쿼리를 추가했습니다.
- **성능 최적화**: 애플리케이션 환경이 안전한 `textContent` DOM API만을 사용하여 렌더링되므로, 불필요한 HTML Sanitize 라이브러리(`DOMPurify`) 로딩 스크립트와 `security.js`를 제거하여 빌드/배포 크기를 줄이고 초기 로딩 성능을 개선했습니다.
- **보안 강화**: DOM XSS 공격을 방지하기 위해 CSP에 `require-trusted-types-for 'script'`를 추가했습니다. 현재 애플리케이션은 `textContent`와 같은 안전한 DOM API만 사용하므로 외부 라이브러리 없이 네이티브 보호가 가능합니다.
- **UX 개선**: 내비게이션 링크(`.site-nav a`, `.intro-lnb a`)에 호버 시 부드러운 색상 전환 트랜지션을 추가했습니다.
- **성능 개선**: `i18n.js`에서 초기 로드 시 기본 언어가 한국어(ko)인 경우 불필요한 DOM 순회 및 텍스트 업데이트를 생략하도록 개선했습니다.
- **테스트 추가**: 다국어 처리 로직의 무결성을 검증하기 위해 `test_i18n.html` 테스트 파일을 추가했습니다.
