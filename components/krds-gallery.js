    // ⚡ Bolt: Use event delegation for tabs to reduce event listeners and avoid O(n^2) updates
    document.addEventListener("click", (e) => {
      const tab = e.target.closest('[role="tab"]');
      if (tab) {
        const tabsContainer = tab.closest('.krds-tabs');
        if (tabsContainer) {
          const currentTab = tabsContainer.querySelector('[role="tab"][aria-selected="true"]');
          if (currentTab && currentTab !== tab) {
            currentTab.setAttribute("aria-selected", "false");
            document.getElementById(currentTab.getAttribute("aria-controls")).hidden = true;
          }
          if (currentTab !== tab) {
            tab.setAttribute("aria-selected", "true");
            document.getElementById(tab.getAttribute("aria-controls")).hidden = false;
          }
        }
        return;
      }

      // ⚡ Bolt: Use event delegation for tag removal
      const removeBtn = e.target.closest('.krds-tag__remove');
      if (removeBtn) {
        removeBtn.closest('.krds-tag').remove();
      }
    });
