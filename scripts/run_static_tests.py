#!/usr/bin/env python3
"""Run the repository's parameter-free static-site regression tests.

The site intentionally has no runtime Python package or third-party test
framework dependency. This runner imports each ``tests/test_*.py`` module,
executes its locally defined ``test_*`` functions in deterministic order, and
fails closed if a future test introduces parameters that would require fixture
semantics the runner cannot honestly provide.
"""

from __future__ import annotations

import importlib.util
import inspect
import sys
import traceback
from collections.abc import Callable, Iterator
from pathlib import Path
from types import ModuleType


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
TESTS_DIRECTORY = REPOSITORY_ROOT / "tests"
TestFunction = Callable[[], None]


def load_test_module(test_path: Path) -> ModuleType:
    """Import one test module from its exact repository path."""
    module_name = f"_cwl_static_tests_{test_path.stem}"
    spec = importlib.util.spec_from_file_location(module_name, test_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot create an import specification for {test_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def iter_test_functions(module: ModuleType) -> Iterator[tuple[str, TestFunction]]:
    """Yield locally defined, parameter-free tests in deterministic order."""
    for name, test_function in inspect.getmembers(module, inspect.isfunction):
        if not name.startswith("test_") or test_function.__module__ != module.__name__:
            continue

        signature = inspect.signature(test_function)
        if signature.parameters:
            raise TypeError(
                f"{module.__name__}.{name} declares parameters; "
                "this dependency-free runner supports parameter-free tests only"
            )
        yield name, test_function


def main() -> int:
    """Execute every discovered test and return a process-compatible status."""
    sys.path.insert(0, str(REPOSITORY_ROOT))
    test_paths = sorted(TESTS_DIRECTORY.glob("test_*.py"))
    if not test_paths:
        print("static test runner: no test modules found", file=sys.stderr)
        return 1

    executed = 0
    failures = 0
    for test_path in test_paths:
        try:
            module = load_test_module(test_path)
            test_functions = list(iter_test_functions(module))
            if not test_functions:
                raise RuntimeError(f"{test_path} defines no test functions")
        except Exception:
            failures += 1
            print(f"ERROR collecting {test_path.relative_to(REPOSITORY_ROOT)}")
            traceback.print_exc()
            continue

        for test_name, test_function in test_functions:
            executed += 1
            test_id = f"{test_path.name}::{test_name}"
            try:
                test_function()
            except Exception:
                failures += 1
                print(f"FAIL {test_id}")
                traceback.print_exc()
            else:
                print(f"PASS {test_id}")

    if executed == 0:
        print("static test runner: zero tests executed", file=sys.stderr)
        return 1
    if failures:
        print(f"static test runner: {failures} failure(s), {executed} test(s) executed")
        return 1

    print(f"static test runner: {executed} test(s) passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
