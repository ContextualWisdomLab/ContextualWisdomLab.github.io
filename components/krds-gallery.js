// Tabs: WAI-ARIA roving tabindex with automatic activation for local content.
document.querySelectorAll(".krds-tabs").forEach((tabs) => {
  const tabList = [...tabs.querySelectorAll('[role="tab"]')];

  const activateTab = (nextTab, moveFocus = false) => {
    tabList.forEach((tab) => {
      const isSelected = tab === nextTab;
      const panelId = tab.getAttribute("aria-controls");
      const panel = panelId === null ? null : document.getElementById(panelId);

      tab.setAttribute("aria-selected", String(isSelected));
      tab.setAttribute("tabindex", isSelected ? "0" : "-1");
      if (panel !== null) {
        panel.hidden = !isSelected;
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
  button.addEventListener("click", () => button.closest(".krds-tag").remove())
);
