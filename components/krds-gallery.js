// Tabs: WAI-ARIA roving tabindex with automatic activation for local content.
document.querySelectorAll(".krds-tabs").forEach((tabs) => {
  const tabList = [...tabs.querySelectorAll('[role="tab"]')];

  const activateTab = (nextTab, moveFocus = false) => {
    const tabPanels = tabList.map((tab) => {
      const panelId = tab.getAttribute("aria-controls");
      const panel = panelId === null ? null : document.getElementById(panelId);
      return { tab, panel };
    });

    if (tabPanels.some(({ panel }) => panel === null)) {
      console.warn("[Security] Requested tab panel is unavailable.");
      return;
    }

    tabPanels.forEach(({ tab, panel }) => {
      const isSelected = tab === nextTab;

      // ⚡ Bolt: Avoid redundant DOM mutations to prevent style invalidation and layout thrashing
      const newAriaSelected = String(isSelected);
      if (tab.getAttribute("aria-selected") !== newAriaSelected) {
        tab.setAttribute("aria-selected", newAriaSelected);
      }

      const newTabIndex = isSelected ? "0" : "-1";
      if (tab.getAttribute("tabindex") !== newTabIndex) {
        tab.setAttribute("tabindex", newTabIndex);
      }

      const newHidden = !isSelected;
      if (panel.hidden !== newHidden) {
        panel.hidden = newHidden;
      }
    });

    if (moveFocus) {
      nextTab.focus();
    }
  };

  tabList.forEach((tab, index) => {
    tab.addEventListener("click", () => activateTab(tab));

    tab.addEventListener("keydown", (event) => {
      let nextIndex;

      switch (event.key) {
        case "ArrowRight":
          nextIndex = (index + 1) % tabList.length;
          break;
        case "ArrowLeft":
          nextIndex = (index - 1 + tabList.length) % tabList.length;
          break;
        case "Home":
          nextIndex = 0;
          break;
        case "End":
          nextIndex = tabList.length - 1;
          break;
        default:
          return;
      }

      event.preventDefault();
      activateTab(tabList[nextIndex], true);
    });
  });
});

// Tag remove
// Native buttons preserve keyboard activation and accessible names.
document.querySelectorAll(".krds-tag__remove").forEach((button) =>
  button.addEventListener("click", () => {
    const tag = button.closest(".krds-tag");
    if (tag === null) {
      console.warn("[Security] Tag container is unavailable.");
      return;
    }
    tag.remove();
  })
);
