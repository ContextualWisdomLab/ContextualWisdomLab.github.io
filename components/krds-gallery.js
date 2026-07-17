    // Tabs: minimal roving behavior. ponytail: native buttons + aria, no framework.
    document.querySelectorAll(".krds-tabs").forEach((tabs) => {
      const tabList = [...tabs.querySelectorAll('[role="tab"]')];

      const selectTab = (tab) => {
        tabList.forEach((t) => {
          const sel = t === tab;
          t.setAttribute("aria-selected", sel);
          t.setAttribute("tabindex", sel ? "0" : "-1");
          document.getElementById(t.getAttribute("aria-controls")).hidden = !sel;
        });
        tab.focus();
      };

      tabList.forEach((tab, index) => {
        tab.addEventListener("click", () => selectTab(tab));

        tab.addEventListener("keydown", (e) => {
          if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
            e.preventDefault();
            const direction = e.key === "ArrowRight" ? 1 : -1;
            const newIndex = (index + direction + tabList.length) % tabList.length;
            selectTab(tabList[newIndex]);
          }
        });
      });
    });
    // Tag remove
    document.querySelectorAll(".krds-tag__remove").forEach((btn) =>
      btn.addEventListener("click", () => btn.closest(".krds-tag").remove())
    );
