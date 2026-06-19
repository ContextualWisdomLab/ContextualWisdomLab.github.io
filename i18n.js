const messages = {
  ko: {
    metaTitle: "맥락지혜 연구실 | Contextual Wisdom Lab",
    metaDescription: "맥락지혜 연구실은 흩어진 기업 자료를 맥락 안에서 판단 가능한 구조로 바꾸는 AI 의사결정 지원 시스템을 연구하고 만듭니다.",
    logoSrc: "assets/context-wisdom-lab-logo.svg",
    logoAlt: "맥락지혜 연구실 · Contextual Wisdom Lab",
    "nav.intro": "소개",
    "nav.problem": "문제의식",
    "nav.model": "연구모형",
    "nav.evidence": "근거",
    "nav.contextualWisdom": "이름 뜻",
    "nav.principles": "원칙",
    "nav.dikw": "DIKW",
    "nav.logo": "로고",
    "nav.work": "작업",
    "hero.title": "맥락지혜 연구실",
    "hero.labName": "Contextual Wisdom Lab",
    "hero.thesis": "구슬이 서 말이어도 꿰어야 보배이듯, 문서, 메일, 로그, 회의록을 맥락 안에서 엮어 사람이 무엇을 결정하고 무엇을 실행할지 보이게 하는 AI 의사결정 지원 시스템을 연구하고 만듭니다.",
    "hero.primaryCta": "GitHub 보기",
    "hero.secondaryCta": "DIKW 보기",
    "ladder.data": "기록된 흔적 · 문서 · 메일 · 로그",
    "ladder.information": "질문과 기준 안에서 해석된 자료",
    "ladder.knowledge": "관계, 원인, 제약으로 설명되는 구조",
    "ladder.wisdom": "판단과 실행으로 건너가기",
    "principles.title": "맥락지혜는 맥락 안에서 판단을 세우는 방향입니다",
    "principles.lead": "Contextual Wisdom은 많이 아는 상태가 아니라, 구체적인 맥락 안에서 판단과 실행으로 건너가는 과정을 뜻합니다. 메일, 문서, 로그, 일정 사이의 흩어진 맥락을 묶어 오늘 결정할 것과 다음 행동을 보이게 합니다.",
    "principles.oneTitle": "앞뒤 사정 보기",
    "principles.oneBody": "같은 말과 기록도 상황이 바뀌면 뜻이 달라집니다. 목적, 제약, 이해관계, 시간 압박을 함께 봅니다.",
    "principles.twoTitle": "종합은 요약이 아닙니다",
    "principles.twoBody": "길이를 줄이는 데서 멈추지 않습니다. 증거, 맥락, 리스크, 선택지를 엮어 사람이 판단할 수 있는 구조를 만듭니다.",
    "principles.threeTitle": "실행으로 이어가기",
    "principles.threeBody": "좋은 구조는 읽고 끝나지 않습니다. 결정할 것, 확인할 가정, 다음 행동, 위임과 기록으로 이어져야 합니다.",
    "problem.title": "시작점은 인지 부하입니다",
    "problem.lead": "정보가 부족해서가 아니라, 판단해야 할 맥락이 흩어져 있어서 어렵습니다. 사람이 버거워지는 순간은 데이터가 많을 때가 아니라 맥락을 다시 조립해야 할 때입니다.",
    "problem.oneTitle": "흩어진 자료",
    "problem.oneBody": "메일, 문서, 로그, VOC, 회의록, 일정이 각자의 저장소에 남습니다.",
    "problem.twoTitle": "사라지는 기준",
    "problem.twoBody": "누가 무엇을 기준으로 판단했는지 시간이 지나면 흐려집니다.",
    "problem.threeTitle": "필요한 구조",
    "problem.threeBody": "오늘 결정할 것, 확인할 가정, 다음 행동이 보이는 구조가 필요합니다.",
    "dikw.title": "DIKW는 판단 흐름을 점검하는 질문입니다",
    "dikw.lead": "PPTX의 흐름은 기업 자료, 맥락화, 판단 포인트, 실행 연결입니다. DIKW는 이 흐름을 자동 상승 위계로 보자는 말이 아니라, 자료가 판단 근거로 쓰일 준비가 되었는지 묻는 점검 질문입니다.",
    "dikw.dataTitle": "기업 자료",
    "dikw.dataBody": "문서, 메일, 로그, VOC, 일정은 아직 증거로 해석되기 전의 기록입니다.",
    "dikw.infoTitle": "맥락화",
    "dikw.infoBody": "누가, 언제, 어디서, 어떤 목적과 기준으로 남긴 것인지 알 때 정보가 됩니다.",
    "dikw.knowledgeTitle": "판단 포인트",
    "dikw.knowledgeBody": "원인, 패턴, 예외, 제약, 절차가 연결될 때 한 사례를 넘어 쓸 수 있는 구조가 됩니다.",
    "dikw.wisdomTitle": "실행 연결",
    "dikw.wisdomBody": "목적과 제약 안에서 가치, 트레이드오프, 반례, 실패 가능성을 드러내고 무엇을 할지 선택한 뒤 다음 행동으로 연결합니다.",
    "evidence.title": "논문 리뷰에서 남긴 경계",
    "evidence.lead": "홈페이지 문장은 연구 근거가 허용하는 만큼만 말합니다. 그래서 쓰는 표현과 버린 표현을 구분합니다.",
    "evidence.dikwTitle": "DIKW: 유용한 구분, 위험한 피라미드",
    "evidence.dikwBody": "Ackoff는 data, information, knowledge, wisdom의 구분을 제시했지만 Rowley, Baskarada와 Koronios, Frické는 정의 합의 부족과 선형 위계의 취약성을 지적합니다. 그래서 자동 상승 모델로 쓰지 않습니다.",
    "evidence.wisdomTitle": "Wisdom: 많이 아는 것이 아니라 맥락에서 판단하는 것",
    "evidence.wisdomBody": "Baltes와 Staudinger, Sternberg 계열의 지혜 연구는 생애 문제, 가치 균형, 불확실성, 실천적 판단을 다룹니다. 지혜는 단순한 정보량보다 판단 조건에 가깝습니다.",
    "evidence.situatedTitle": "Wisdom: 상황 안에서 달라지는 판단",
    "evidence.situatedBody": "Grossmann과 Brienza의 situated wise reasoning 연구는 지혜 관련 추론이 구체적 상황과 관점에 따라 달라진다는 점을 보여줍니다. 그래서 이 연구실은 지혜를 맥락 밖의 정답으로 말하지 않습니다.",
    "evidence.synthesisTitle": "Synthesis: 요약이 아니라 판단 구조",
    "evidence.synthesisBody": "PPTX의 핵심은 더 짧게 말하는 AI가 아니라, 맥락을 다시 조립하는 인지 부하를 줄이는 DSS입니다. 자료는 판단 포인트와 실행 연결을 만들 때 비로소 쓸모가 생깁니다.",
    "logo.title": "로고는 상승보다 연결을 그립니다",
    "logo.lead": "겹친 블록은 흩어진 기록을, 선은 그 기록이 특정 질문과 제약 속에서 연결되는 경로를 뜻합니다. 마지막 금색 점은 자동 도달점이 아니라 사람이 책임 있게 선택해야 하는 판단 순간입니다.",
    "logo.layerTitle": "Layered context",
    "logo.layerBody": "문서, 메일, 로그, VOC처럼 분산된 단서가 하나의 구조로 겹쳐집니다.",
    "logo.pathTitle": "Contextual path",
    "logo.pathBody": "선은 자료가 스스로 올라가는 길이 아니라 질문, 기준, 반례 검토를 통과해 판단과 실행으로 건너가는 과정입니다.",
    "logo.colorTitle": "Color system",
    "logo.colorBody": "짙은 남색은 판단의 기준, 틸은 맥락화, 금색은 선택과 실행을 나타냅니다.",
    "work.title": "오늘의 초점",
    "work.lead": "LLM 시스템이 분산된 기업 자료의 맥락을 이어 어떻게 낮은 인지 부하의 판단과 실행으로 바꿀 수 있는지 탐구합니다. 목표는 개인은 덜 소모되고 조직은 더 원활하게 움직이도록 돕는 것입니다. Naruon은 이 문제를 메일 흐름에서 검증하는 제품 실험입니다.",
    "work.oneTitle": "Context systems",
    "work.oneBody": "관계, 출처, 기준, 리스크를 함께 보존하는 지식 구조.",
    "work.twoTitle": "Decision interfaces",
    "work.twoBody": "오늘 결정할 것과 확인할 가정을 드러내는 화면.",
    "work.threeTitle": "Enterprise AI rails",
    "work.threeBody": "인증, 권한, 보안, 감사, 사용량 책임이 작동하는 운영 기반.",
    "work.fourTitle": "Agentic workflows",
    "work.fourBody": "반복 탐색은 줄이고 근거 확인과 사람의 판단은 남기는 흐름.",
    "footer.founded": "Founded by",
    "footer.line": "Context into judgment. Judgment into action."
  },
  en: {
    metaTitle: "Contextual Wisdom Lab",
    metaDescription: "A research lab building AI decision support systems that connect scattered enterprise material into judgment inside concrete contexts.",
    logoSrc: "assets/context-wisdom-lab-logo-en.svg",
    logoAlt: "Contextual Wisdom Lab",
    "nav.intro": "Intro",
    "nav.problem": "Problem",
    "nav.model": "Research Model",
    "nav.evidence": "Evidence",
    "nav.contextualWisdom": "Name",
    "nav.principles": "Principles",
    "nav.dikw": "DIKW",
    "nav.logo": "Logo",
    "nav.work": "Work",
    "hero.title": "Contextual Wisdom Lab",
    "hero.labName": "Research Lab",
    "hero.thesis": "A research lab building AI decision support systems. Even a heap of beads becomes treasure only when threaded; we compose context across documents, mail, logs, and meeting notes so people can see what to decide and what to do next.",
    "hero.primaryCta": "Explore GitHub",
    "hero.secondaryCta": "Read DIKW",
    "ladder.data": "Recorded traces · documents · mail · logs",
    "ladder.information": "Material interpreted inside a question",
    "ladder.knowledge": "Structure explained by relations and constraints",
    "ladder.wisdom": "Crossing into judgment and action",
    "principles.title": "Contextual Wisdom means judgment inside context",
    "principles.lead": "맥락지혜 연구실 is the Korean name for Contextual Wisdom Lab. Contextual Wisdom means crossing from scattered material into judgment and action inside a concrete context.",
    "principles.oneTitle": "See the circumstances",
    "principles.oneBody": "The same words and records can mean different things in different situations. We look at purpose, constraints, stakeholders, and time pressure together.",
    "principles.twoTitle": "Synthesis is not summary",
    "principles.twoBody": "We do not stop at shortening text. We connect evidence, context, risk, and options into a structure people can judge with.",
    "principles.threeTitle": "Cross into action",
    "principles.threeBody": "A good structure does not end at reading. It should lead to decisions, assumptions to verify, next actions, delegation, and records.",
    "problem.title": "The starting point is cognitive load",
    "problem.lead": "The hard part is not the lack of information. It is that the context needed for judgment is scattered. People become overloaded when they must rebuild context by hand.",
    "problem.oneTitle": "Scattered material",
    "problem.oneBody": "Mail, documents, logs, VOC, meeting notes, and schedules remain in separate places.",
    "problem.twoTitle": "Fading criteria",
    "problem.twoBody": "Over time, it becomes unclear who judged what and by which standard.",
    "problem.threeTitle": "Needed structure",
    "problem.threeBody": "People need to see what to decide today, which assumptions to verify, and what to do next.",
    "dikw.title": "DIKW is not a hierarchy; it is a set of questions",
    "dikw.lead": "The original frame offers useful distinctions, but later work warns about definitional confusion and linear conversion claims. We do not treat the pyramid as a factual model; we use it to ask whether material is ready to support judgment inside context.",
    "dikw.dataTitle": "What was recorded?",
    "dikw.dataBody": "Documents, mail, logs, VOC, and schedules are records before they become evidence.",
    "dikw.infoTitle": "Which question does it answer?",
    "dikw.infoBody": "Material becomes informative when we know who created it, when, where, under what criteria, and for which purpose.",
    "dikw.knowledgeTitle": "What does it explain?",
    "dikw.knowledgeBody": "Causes, patterns, exceptions, constraints, and procedures make information usable beyond one case.",
    "dikw.wisdomTitle": "What should be done in this context?",
    "dikw.wisdomBody": "Wisdom makes values, trade-offs, counterevidence, and fallibility visible, then connects the choice to the next action.",
    "evidence.title": "Boundaries from the paper review",
    "evidence.lead": "The homepage only says what the literature can bear. We separate the claims we keep from the claims we discard.",
    "evidence.dikwTitle": "DIKW: useful distinction, risky pyramid",
    "evidence.dikwBody": "Ackoff distinguishes data, information, knowledge, and wisdom, but Rowley, Baskarada and Koronios, and Frické warn about unclear definitions and weak linear hierarchy claims. We therefore avoid an automatic ascent model.",
    "evidence.wisdomTitle": "Wisdom: judgment in context, not mere accumulation",
    "evidence.wisdomBody": "Work by Baltes, Staudinger, Sternberg, and others connects wisdom with life problems, value balancing, uncertainty, and practical judgment. It is closer to conditions for judgment than to quantity of information.",
    "evidence.situatedTitle": "Wisdom: judgment changes by situation",
    "evidence.situatedBody": "Grossmann and Brienza's work on situated wise reasoning shows that wisdom-related reasoning varies across situations and perspectives. We therefore avoid treating wisdom as an answer outside context.",
    "evidence.synthesisTitle": "Synthesis: judgment structure, not summary",
    "evidence.synthesisBody": "The PPTX argument is not to make AI shorter. It is to reduce the cognitive load of rebuilding context by turning material into judgment points and action links.",
    "logo.title": "The logo draws connection, not automatic ascent",
    "logo.lead": "The layered blocks represent scattered records. The line shows records being connected inside a concrete question and constraint set. The final gold point is not an automatic destination; it is the moment of responsible judgment.",
    "logo.layerTitle": "Layered context",
    "logo.layerBody": "Documents, mail, logs, VOC, and schedules are brought into one judgment structure.",
    "logo.pathTitle": "Contextual path",
    "logo.pathBody": "The line is not a road that data climbs by itself. It is a process of connecting records through questions, criteria, and counterevidence until they cross into judgment and action.",
    "logo.colorTitle": "Color system",
    "logo.colorBody": "Deep ink stands for judgment, teal for contextualization, and gold for choice and execution.",
    "work.title": "Current focus",
    "work.lead": "We explore how LLM systems can connect the context around distributed enterprise material and turn it into lower-cognitive-load judgment and action, so individuals are less depleted and organizations move more smoothly. Naruon is the product experiment in the email workflow.",
    "work.oneTitle": "Context systems",
    "work.oneBody": "Knowledge structures that preserve relationships, sources, criteria, and risk.",
    "work.twoTitle": "Decision interfaces",
    "work.twoBody": "Interfaces that reveal what to decide today and which assumptions need verification.",
    "work.threeTitle": "Enterprise AI rails",
    "work.threeBody": "Operational foundations for identity, authorization, security, audit, and usage accountability.",
    "work.fourTitle": "Agentic workflows",
    "work.fourBody": "Workflows that reduce repeated search while preserving evidence checks and human judgment.",
    "footer.founded": "Founded by",
    "footer.line": "Context into judgment. Judgment into action."
  }
};

function preferredLanguage() {
  const query = new URLSearchParams(window.location.search).get("lang");
  const saved = localStorage.getItem("cwl-language");
  const browser = navigator.language?.toLowerCase().startsWith("ko") ? "ko" : "en";
  return messages[query] ? query : messages[saved] ? saved : browser;
}

function setLanguage(lang) {
  const dict = messages[lang] || messages.ko;
  document.documentElement.lang = lang;
  document.title = dict.metaTitle;
  document.querySelector('meta[name="description"]')?.setAttribute("content", dict.metaDescription);
  document.querySelector('meta[property="og:description"]')?.setAttribute("content", dict.metaDescription);
  const footerLogo = document.querySelector("#footer-logo");
  if (footerLogo) {
    footerLogo.src = dict.logoSrc;
    footerLogo.alt = dict.logoAlt;
  }
  document.querySelectorAll("[data-i18n]").forEach((node) => {
    node.textContent = dict[node.dataset.i18n] || node.textContent;
  });
  document.querySelectorAll("[data-lang]").forEach((button) => {
    button.setAttribute("aria-pressed", String(button.dataset.lang === lang));
  });
  localStorage.setItem("cwl-language", lang);
}

document.querySelectorAll("[data-lang]").forEach((button) => {
  button.addEventListener("click", () => setLanguage(button.dataset.lang));
});

setLanguage(preferredLanguage());
