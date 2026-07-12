import re

with open("CHANGELOG.md", "r", encoding="utf-8") as f:
    content = f.read()

# Already documented in the previous commit message:
# - **UX/접근성 개선**: `.dikw-grid span`의 텍스트 색상을 `var(--gold)`에서 `var(--teal)`로 변경하여 밝은 배경에서의 대비(Color Contrast)를 개선하고 WCAG 접근성 기준을 충족하도록 하였습니다.

# We will just verify if the text is there to ensure we do not need to add it again
if "var(--teal)" in content:
    print("Already in CHANGELOG.md")
else:
    print("Not in CHANGELOG.md")
