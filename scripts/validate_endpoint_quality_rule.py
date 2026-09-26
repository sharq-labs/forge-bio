from __future__ import annotations

"""Compatibility CLI for the canonical endpoint-quality executor.

There is exactly one scientific source of truth for endpoint field semantics:
scripts.evaluate_endpoint_quality. This module intentionally contains no
independent registry or validation logic.
"""

import argparse
import json
from pathlib import Path

from scripts.evaluate_endpoint_quality import (
    evaluate_rule,
    load_json,
    validate_rule,
)


# Backward-compatible API names. They delegate to the canonical implementation.
validate_rule_semantics = validate_rule
evaluate_event = evaluate_rule


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Compatibility wrapper for the canonical endpoint-quality executor"
    )
    ap.add_argument("rule", type=Path)
    ap.add_argument("--event", type=Path)
    args = ap.parse_args()

    rule = load_json(args.rule)
    errors = validate_rule(rule)
    if errors:
        for err in errors:
            print(err)
        return 1

    if args.event is not None:
        event = load_json(args.event)
        passed, failures = evaluate_rule(rule, event)
        print(json.dumps({"passed": passed, "failures": failures}, indent=2, allow_nan=False))
        return 0 if passed else 2

    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
