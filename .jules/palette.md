## 2024-05-18 - Click Feedback for Interactive Elements
**Learning:** 시각적 호버 상태(opacity change)만으로는 사용자가 클릭이 성공적으로 이루어졌는지 즉시 체감하기 어렵습니다. 물리적인 버튼처럼 눌리는 피드백이 필요합니다.
**Action:** 클릭 가능한 주요 버튼 요소에 `transform: scale(0.96)` 등의 미세한 스케일 축소를 `:active` 상태에 적용하여 즉각적이고 부드러운 촉각적(Tactile) 시각 피드백을 제공하도록 합니다.
