    // Tabs: minimal roving behavior. ponytail: native buttons + aria, no framework.
    document.querySelectorAll(".krds-tabs").forEach((tabs) => {
      const tabList = [...tabs.querySelectorAll('[role="tab"]')];
      tabList.forEach((tab) => {
        tab.addEventListener("click", () => {
          tabList.forEach((t) => {
            const sel = t === tab;
            t.setAttribute("aria-selected", sel);
            document.getElementById(t.getAttribute("aria-controls")).hidden = !sel;
          });
        });
      });
    });
    // Tag remove
    document.querySelectorAll(".krds-tag__remove").forEach((btn) =>
      btn.addEventListener("click", () => btn.closest(".krds-tag").remove())
    );
