"""Runtime regressions for component-gallery interaction and DOM integrity."""

from __future__ import annotations

import subprocess
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
GALLERY_SCRIPT = REPOSITORY_ROOT / "components" / "krds-gallery.js"


def _run_gallery_harness(harness: str) -> subprocess.CompletedProcess[str]:
    """Execute a dependency-free Node harness against the checked-in gallery script."""
    return subprocess.run(
        ["node", "-e", harness],
        input=GALLERY_SCRIPT.read_text(encoding="utf-8"),
        capture_output=True,
        check=False,
        text=True,
    )


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
    completed = _run_gallery_harness(harness)
    assert completed.returncode == 0, completed.stderr


def test_valid_target_does_not_mutate_when_sibling_panel_mapping_is_broken() -> None:
    """A corrupt tab set must fail atomically before changing selection or focus."""
    harness = r'''
const fs = require("node:fs");
const script = fs.readFileSync(0, "utf8");
const warnings = [];
const listeners = new Map();
let focusCount = 0;

function tab(name, panelId, selected, tabIndex) {
  return {
    name,
    attributes: {
      "aria-controls": panelId,
      "aria-selected": selected,
      "tabindex": tabIndex,
    },
    addEventListener(type, callback) { listeners.set(`${name}:${type}`, callback); },
    getAttribute(attribute) { return this.attributes[attribute] ?? null; },
    setAttribute(attribute, value) { this.attributes[attribute] = String(value); },
    focus() { focusCount += 1; },
  };
}

const activeTab = tab("active", "active-panel", "true", "0");
const nextTab = tab("next", "next-panel", "false", "-1");
const brokenSibling = tab("broken", "untrusted\nmissing-panel", "false", "-1");
const activePanel = {hidden: false};
const nextPanel = {hidden: true};
const tabGroup = {querySelectorAll: () => [activeTab, nextTab, brokenSibling]};

global.document = {
  querySelectorAll(selector) {
    if (selector === ".krds-tabs") return [tabGroup];
    if (selector === ".krds-tag__remove") return [];
    return [];
  },
  getElementById(identifier) {
    if (identifier === "active-panel") return activePanel;
    if (identifier === "next-panel") return nextPanel;
    return null;
  },
};
console.warn = (message) => warnings.push(String(message));

eval(script);
listeners.get("next:click")();

if (activeTab.attributes["aria-selected"] !== "true" || activeTab.attributes.tabindex !== "0" ||
    nextTab.attributes["aria-selected"] !== "false" || nextTab.attributes.tabindex !== "-1" ||
    brokenSibling.attributes["aria-selected"] !== "false" || brokenSibling.attributes.tabindex !== "-1" ||
    activePanel.hidden !== false || nextPanel.hidden !== true || focusCount !== 0) {
  throw new Error("corrupt sibling mapping allowed a partial tab-set mutation");
}
if (warnings.length !== 1 || warnings[0] !== "[Security] Requested tab panel is unavailable.") {
  throw new Error(`unexpected warnings: ${JSON.stringify(warnings)}`);
}
if (warnings[0].includes("untrusted")) {
  throw new Error("untrusted panel identifiers reached warning output");
}
'''
    completed = _run_gallery_harness(harness)
    assert completed.returncode == 0, completed.stderr


def test_keyboard_navigation_executes_wrapped_state_transitions() -> None:
    """Arrow, Home, and End keys execute APG-style wrapping and state changes."""
    harness = r'''
const fs = require("node:fs");
const script = fs.readFileSync(0, "utf8");
const listeners = new Map();
let focusedName = null;

function tab(name, panelId, selected, tabIndex) {
  return {
    name,
    attributes: {
      "aria-controls": panelId,
      "aria-selected": selected,
      "tabindex": tabIndex,
    },
    addEventListener(type, callback) { listeners.set(`${name}:${type}`, callback); },
    getAttribute(attribute) { return this.attributes[attribute] ?? null; },
    setAttribute(attribute, value) { this.attributes[attribute] = String(value); },
    focus() { focusedName = name; },
  };
}

const tabs = [
  tab("first", "panel-first", "true", "0"),
  tab("middle", "panel-middle", "false", "-1"),
  tab("last", "panel-last", "false", "-1"),
];
const panels = {
  "panel-first": {hidden: false},
  "panel-middle": {hidden: true},
  "panel-last": {hidden: true},
};
const tabGroup = {querySelectorAll: () => tabs};

global.document = {
  querySelectorAll(selector) {
    if (selector === ".krds-tabs") return [tabGroup];
    if (selector === ".krds-tag__remove") return [];
    return [];
  },
  getElementById(identifier) { return panels[identifier] ?? null; },
};
console.warn = (message) => { throw new Error(`unexpected warning: ${message}`); };

eval(script);

function assertState(expectedIndex) {
  tabs.forEach((candidate, index) => {
    const selected = index === expectedIndex;
    if (candidate.attributes["aria-selected"] !== String(selected)) {
      throw new Error(`${candidate.name} aria-selected mismatch`);
    }
    if (candidate.attributes.tabindex !== (selected ? "0" : "-1")) {
      throw new Error(`${candidate.name} tabindex mismatch`);
    }
    const panel = panels[candidate.attributes["aria-controls"]];
    if (panel.hidden !== !selected) {
      throw new Error(`${candidate.name} panel hidden state mismatch`);
    }
  });
}

function press(tabName, key) {
  const event = {
    key,
    prevented: false,
    preventDefault() { this.prevented = true; },
  };
  const handler = listeners.get(`${tabName}:keydown`);
  if (!handler) throw new Error(`missing keydown listener for ${tabName}`);
  handler(event);
  return event;
}

assertState(0);

let event = press("first", "ArrowLeft");
if (!event.prevented || focusedName !== "last") throw new Error("ArrowLeft did not wrap to last");
assertState(2);

event = press("last", "ArrowRight");
if (!event.prevented || focusedName !== "first") throw new Error("ArrowRight did not wrap to first");
assertState(0);

event = press("first", "End");
if (!event.prevented || focusedName !== "last") throw new Error("End did not activate last");
assertState(2);

event = press("last", "Home");
if (!event.prevented || focusedName !== "first") throw new Error("Home did not activate first");
assertState(0);

event = press("first", "Tab");
if (event.prevented) throw new Error("unhandled Tab key was prevented");
if (focusedName !== "first") throw new Error("unhandled Tab key moved scripted focus");
assertState(0);
'''
    completed = _run_gallery_harness(harness)
    assert completed.returncode == 0, completed.stderr
