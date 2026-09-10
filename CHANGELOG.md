# CHANGELOG

## [Unreleased]
- **고객 경험 개선**: GitHub Pages 기본 404 페이지 대신 브랜드가 적용된 `404.html`을 추가했습니다. 잘못된 주소로 들어온 방문자는 그동안 안내 없는 기본 오류 화면을 봤지만, 이제 연구실 색·서체·내비게이션 안에서 "페이지를 찾을 수 없습니다" 안내와 홈·프로젝트로 돌아가는 링크를 봅니다. 페이지는 `noindex`로 검색 색인에서 제외하고, 자체 CSS만 사용하는 자족형 문서라 CSP를 약화하지 않습니다. 회귀 테스트가 자산 존재·CSP 안전성·noindex·내부 앵커 실재를 검증합니다.
- **링크 미리보기 개선**: 홈페이지의 `og:image`가 상대 경로여서 Open Graph 크롤러가 이미지를 찾지 못하고 공유 링크에 미리보기가 표시되지 않던 문제를 수정했습니다. 절대 URL 이미지와 `og:url`·`og:site_name`·`og:locale`·이미지 크기/대체 텍스트, Twitter `summary` 카드, `rel="canonical"`을 추가하고, 언어 전환 시 `twitter:description`도 함께 갱신합니다.
- **보안 개선**: `i18n.js`에서 잘못된 언어 요청 시 `console.warn` 메시지에 사용자 입력값이 직접 포함되지 않도록 수정하여 로그 인젝션(Log Injection) 취약점을 제거했습니다.
- **성능 개선**: `.skip-link` 애니메이션을 `top`에서 `transform: translateY()`로 변경하여 전환 중 레이아웃 재계산을 줄일 수 있도록 했습니다. 실제 효과는 브라우저별 측정 대상입니다.
- **렌더링 힌트 정합성**: 첫 화면의 eager 이미지와 단일 LCP 후보에서 강제 `decoding="async"`를 제거해 HTML 표준의 기본 `auto` 판단에 맡기고, 지연 로드 이미지에는 비동기 디코딩 힌트를 유지했습니다. 정적 테스트가 eager, lazy, LCP 후보 집합의 존재와 조합을 검증하며, 실제 LCP 효과는 배포 후 실측 대상으로 유지합니다.
- **UX/접근성 개선**: 프로젝트 카드의 클릭 영역을 카드 전체로 확장하여 사용자 편의성을 높였습니다. <a> 태그를 확장하는 대신 가상 요소(pseudo-element) 겹침 방식을 사용하여 스크린 리더 접근성을 유지했습니다.
- **보안 개선**: 컴포넌트 갤러리의 인라인 스크립트와 스타일을 외부 파일로 분리하고, 엄격한 Content-Security-Policy를 적용해 XSS 방어를 강화했습니다.
- **성능 회귀 복원**: 오프스크린 `.section` 렌더링을 `content-visibility: auto`로 지연하고, 일반 섹션은 600px·콘텐츠가 큰 DIKW/projects 섹션은 1000px의 `contain-intrinsic-size` placeholder를 유지해 초기 렌더링 비용과 스크롤바 이동을 함께 줄였습니다.
- **보안 개선**: Trusted Types 기반 CSP 강화: 잠재적인 DOM 기반 XSS 공격을 방지하기 위해 `require-trusted-types-for 'script'` 지시어 추가
- **UX/접근성 개선**: `.dikw-grid span`의 텍스트 색상을 `var(--gold)`에서 `var(--teal)`로 변경하여 밝은 배경에서의 대비(Color Contrast)를 개선하고 WCAG 접근성 기준을 충족하도록 하였습니다.
- **UX/접근성 개선**: 시스템 설정에서 '애니메이션 줄이기(prefers-reduced-motion)'를 활성화한 사용자를 위해 과도한 애니메이션과 트랜지션을 비활성화(`0.01ms`)하고 부드러운 스크롤을 끄도록 CSS 미디어 쿼리를 추가했습니다.
- **성능 최적화**: 애플리케이션 환경이 안전한 `textContent` DOM API만을 사용하여 렌더링되므로, 불필요한 HTML Sanitize 라이브러리(`DOMPurify`) 로딩 스크립트와 `security.js`를 제거하여 빌드/배포 크기를 줄이고 초기 로딩 성능을 개선했습니다.
- **보안 강화**: DOM XSS 공격을 방지하기 위해 CSP에 `require-trusted-types-for 'script'`를 추가했습니다. 현재 애플리케이션은 `textContent`와 같은 안전한 DOM API만 사용하므로 외부 라이브러리 없이 네이티브 보호가 가능합니다.
- **UX 개선**: 내비게이션 링크(`.site-nav a`, `.intro-lnb a`)에 호버 시 부드러운 색상 전환 트랜지션을 추가했습니다.
- **보안 개선**: `i18n.js`의 `setLanguage()` 함수에 허용된 언어인지 확인하는 입력값 검증(Input Validation) 로직을 추가하여 Prototype Pollution 및 유효하지 않은 상태 주입을 방지했습니다.
- **성능 개선**: `i18n.js`에서 초기 로드 시 기본 언어가 한국어(ko)인 경우 불필요한 DOM 순회 및 텍스트 업데이트를 생략하도록 개선했습니다.
- **테스트 추가**: 다국어 처리 로직의 무결성을 검증하기 위해 `test_i18n.html` 테스트 파일을 추가했습니다.
- **보안 개선**: 메인 페이지(`index.html`)의 Content-Security-Policy를 `default-src 'none'` 기반의 엄격한 화이트리스트 방식으로 강화하여 잠재적인 공격 표면을 최소화했습니다.
