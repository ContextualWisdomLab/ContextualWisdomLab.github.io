"""Test i18n URLSearchParams execution counts and fallback behavior."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
I18N_SCRIPT = REPOSITORY_ROOT / "i18n.js"


def _run_harness(query_string: str) -> dict:
    """Execute the i18n script with a mocked window.location and URLSearchParams."""
    harness = f"""
    let urlSearchParamsCalls = 0;
    class MockURLSearchParams {{
        constructor(init) {{
            urlSearchParamsCalls++;
            this.params = new Map();
            if (init === "?lang=ko") this.params.set("lang", "ko");
            if (init === "?lang=en") this.params.set("lang", "en");
            if (init === "?lang=fr") this.params.set("lang", "fr");
        }}
        get(key) {{
            return this.params.get(key) || null;
        }}
    }}

    global.window = {{
        location: {{
            search: {json.dumps(query_string)}
        }},
        localStorage: {{
            getItem: () => null
        }}
    }};
    global.navigator = {{
        language: "ja"
    }};

    // Stub DOM methods used by the script
    global.document = {{
        documentElement: {{ setAttribute: () => {{}}, lang: "ja" }},
        title: "",
        querySelector: () => null,
        querySelectorAll: () => []
    }};

    // Eval the script source provided via stdin, replacing URLSearchParams with our mock
    const fs = require('fs');
    let source = fs.readFileSync(0, 'utf-8');

    // Prevent the initial execution of setLanguage at the end of i18n.js
    source = source.replace("setLanguage(preferredLanguage());", "");

    const mockedSource = source.replace(/new URLSearchParams/g, 'new MockURLSearchParams');
    eval(mockedSource);

    // Call preferredLanguage which is defined in the script
    urlSearchParamsCalls = 0;
    const lang = preferredLanguage();

    console.log(JSON.stringify({{
        calls: urlSearchParamsCalls,
        lang: lang
    }}));
    """

    result = subprocess.run(
        ["node", "-e", harness],
        input=I18N_SCRIPT.read_text(encoding="utf-8"),
        capture_output=True,
        check=True,
        text=True,
    )
    return json.loads(result.stdout)


def test_empty_query_string_avoids_parser_call():
    """Verify zero query-parser calls for an empty search string."""
    result = _run_harness("")
    assert result["calls"] == 0


def test_supported_ko_query_string_makes_one_call():
    """Verify one query-parser call for a non-empty supported query."""
    result = _run_harness("?lang=ko")
    assert result["calls"] == 1
    assert result["lang"] == "ko"


def test_supported_en_query_string_makes_one_call():
    """Verify one query-parser call for a non-empty supported query."""
    result = _run_harness("?lang=en")
    assert result["calls"] == 1
    assert result["lang"] == "en"


def test_unsupported_query_string_makes_one_call_and_falls_back():
    """Verify one query-parser call but falling back for unsupported lang."""
    result = _run_harness("?lang=fr")
    assert result["calls"] == 1
    # Falls back to navigator.language logic (but we stubbed to "ja", which drops to 'en')
    assert result["lang"] == "en"
