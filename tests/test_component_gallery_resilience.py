"""Runtime regressions for missing component-gallery DOM targets."""

from __future__ import annotations

import subprocess
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
GALLERY_SCRIPT = REPOSITORY_ROOT / "components" / "krds-gallery.js"


def test_missing_panel_and_tag_targets_fail_without_partial_state() -> None:
    """Missing controlled elements warn statically and preserve prior tab state."""
    harness = r'''
const fs = require("node:fs");
const script = fs.readFileSync(0, "utf8");
const warnings = [];
const listeners = new Map();

function tab(name, panelId, selected, tabIndex) {
  return {
    name,
    attributes: {
      "aria-controls": panelId,
      "aria-selected": selected,
      "tabindex": tabIndex,
    },
    addEventListener(type, callback) {
      listeners.set(`${name}:${type}`, callback);
    },
    getAttribute(attribute) {
      return this.attributes[attribute] ?? null;
    },
    setAttribute(attribute, value) {
      this.attributes[attribute] = String(value);
    },
    focus() {
      throw new Error("missing-panel activation must not move focus");
    },
  };
}

const activeTab = tab("active", "active-panel", "true", "0");
const missingTab = tab("missing", "attacker-controlled\nidentifier", "false", "-1");
const activePanel = {hidden: false};
const validTag = {removeCount: 0, remove() { this.removeCount += 1; }};
const validRemove = {
  addEventListener(type, callback) { listeners.set(`valid-remove:${type}`, callback); },
  closest() { return validTag; },
};
const missingRemove = {
  addEventListener(type, callback) { listeners.set(`missing-remove:${type}`, callback); },
  closest() { return null; },
};
const tabGroup = {querySelectorAll: () => [activeTab, missingTab]};

global.document = {
  querySelectorAll(selector) {
    if (selector === ".krds-tabs") return [tabGroup];
    if (selector === ".krds-tag__remove") return [validRemove, missingRemove];
    return [];
  },
  getElementById(identifier) {
    return identifier === "active-panel" ? activePanel : null;
  },
};
console.warn = (message) => warnings.push(String(message));

eval(script);
listeners.get("missing:click")();
listeners.get("valid-remove:click")();
listeners.get("missing-remove:click")();

if (activeTab.attributes["aria-selected"] !== "true" ||
    activeTab.attributes.tabindex !== "0" ||
    missingTab.attributes["aria-selected"] !== "false" ||
    missingTab.attributes.tabindex !== "-1" ||
    activePanel.hidden !== false) {
  throw new Error("missing-panel activation partially mutated the selected tab state");
}
if (validTag.removeCount !== 1) {
  throw new Error(`valid tag removal count was ${validTag.removeCount}`);
}
const expectedWarnings = [
  "[Security] Requested tab panel is unavailable.",
  "[Security] Tag container is unavailable.",
];
if (JSON.stringify(warnings) !== JSON.stringify(expectedWarnings)) {
  throw new Error(`unexpected warnings: ${JSON.stringify(warnings)}`);
}
if (warnings.some((warning) => warning.includes("attacker-controlled"))) {
  throw new Error("untrusted panel identifiers reached warning output");
}
'''
    completed = subprocess.run(
        ["node", "-e", harness],
        input=GALLERY_SCRIPT.read_text(encoding="utf-8"),
        capture_output=True,
        check=False,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
