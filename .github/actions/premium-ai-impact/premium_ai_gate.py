#!/usr/bin/env python3
"""Validate 4L Premium + AI Impact review receipts.

Distribution mirror only. Canonical authority remains the private 4L Orchestrator.
No third-party dependencies are required.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


class GateError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise GateError(f"Missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise GateError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise GateError(f"{path} must contain a JSON object")
    return value


def validate_rubric(rubric: dict[str, Any]) -> None:
    dimensions = rubric.get("dimensions")
    if not isinstance(dimensions, dict) or not dimensions:
        raise GateError("Rubric must define dimensions")
    weights = []
    for key, definition in dimensions.items():
        if not isinstance(definition, dict):
            raise GateError(f"Dimension {key!r} must be an object")
        weight = definition.get("weight")
        if not isinstance(weight, (int, float)) or isinstance(weight, bool) or weight <= 0:
            raise GateError(f"Dimension {key!r} has invalid weight")
        weights.append(float(weight))
    if not math.isclose(sum(weights), 1.0, rel_tol=0.0, abs_tol=1e-9):
        raise GateError(f"Dimension weights must total 1.0; got {sum(weights):.6f}")
    thresholds = rubric.get("thresholds")
    if not isinstance(thresholds, dict):
        raise GateError("Rubric must define thresholds")
    for mode_key in ("candidate", "public_release"):
        value = thresholds.get(mode_key)
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not 0 <= value <= 100:
            raise GateError(f"Invalid threshold for {mode_key}")
    for gate_group in ("hard_gates", "public_release_gates"):
        values = rubric.get(gate_group)
        if not isinstance(values, list) or not all(isinstance(item, str) and item for item in values):
            raise GateError(f"Rubric {gate_group} must be a list of gate names")
    rules = rubric.get("rules")
    if not isinstance(rules, dict):
        raise GateError("Rubric must define rules")
    if rules.get("quality_pass_does_not_grant_release_authority") is not True:
        raise GateError("Rubric must preserve the release-authority boundary")
    if rules.get("maximum_safe_high_value_automation_default") is not True:
        raise GateError("Rubric must preserve the automation-first default")
    if rules.get("automation_must_not_reduce_quality_or_governance") is not True:
        raise GateError("Rubric must preserve automation quality/governance limits")


def _nonempty_strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


def _validate_automation_assessment(rubric: dict[str, Any], receipt: dict[str, Any]) -> None:
    rules = rubric.get("rules", {})
    if rules.get("maximum_safe_high_value_automation_default") is not True:
        return
    automation = receipt.get("automation")
    if not isinstance(automation, dict):
        raise GateError("Receipt must document an automation assessment")
    if automation.get("assessed") is not True:
        raise GateError("Receipt automation.assessed must be true")
    automated_stages = _nonempty_strings(automation.get("automated_stages"))
    retained_controls = _nonempty_strings(automation.get("retained_human_controls"))
    rationale = str(automation.get("no_additional_automation_rationale", "")).strip()
    if not automated_stages and not rationale:
        raise GateError("Automation assessment must list automated stages or explain why no additional safe, high-value automation applies")
    if not retained_controls:
        raise GateError("Automation assessment must identify retained human-control points")
    if not rationale:
        raise GateError("Automation assessment must explain why remaining manual/human-controlled work is retained")


def _score_dimensions(rubric: dict[str, Any], receipt: dict[str, Any]) -> tuple[float, list[str]]:
    dimensions = receipt.get("dimensions")
    if not isinstance(dimensions, dict):
        raise GateError("Receipt must define dimensions")
    weighted = 0.0
    problems: list[str] = []
    for key, definition in rubric["dimensions"].items():
        review = dimensions.get(key)
        if not isinstance(review, dict):
            problems.append(f"missing dimension: {key}")
            continue
        score = review.get("score")
        if not isinstance(score, (int, float)) or isinstance(score, bool) or not 0 <= score <= 100:
            problems.append(f"invalid score for {key}")
            continue
        evidence = review.get("evidence")
        if not isinstance(evidence, list) or not any(isinstance(item, str) and item.strip() for item in evidence):
            problems.append(f"missing evidence for {key}")
        weighted += float(score) * float(definition["weight"])
    return weighted, problems


def evaluate(rubric: dict[str, Any], receipt: dict[str, Any], mode: str) -> dict[str, Any]:
    if mode not in {"candidate", "public-release"}:
        raise GateError(f"Unsupported mode: {mode}")
    artifact = receipt.get("artifact")
    if not isinstance(artifact, dict) or not str(artifact.get("name", "")).strip():
        raise GateError("Receipt artifact.name is required")
    if not str(artifact.get("version", "")).strip():
        raise GateError("Receipt artifact.version is required")
    ai_uses = receipt.get("ai_uses")
    if not isinstance(ai_uses, list) or not ai_uses:
        raise GateError("Receipt must document at least one AI use")
    for index, use in enumerate(ai_uses, start=1):
        if not isinstance(use, dict):
            raise GateError(f"AI use #{index} must be an object")
        for field in ("purpose", "user_or_production_value", "human_oversight"):
            if not str(use.get(field, "")).strip():
                raise GateError(f"AI use #{index} is missing {field}")
    _validate_automation_assessment(rubric, receipt)
    score, problems = _score_dimensions(rubric, receipt)
    gates = receipt.get("gates")
    if not isinstance(gates, dict):
        raise GateError("Receipt must define gates")
    failed_gates = [gate for gate in rubric["hard_gates"] if gates.get(gate) is not True]
    release_failed: list[str] = []
    if mode == "public-release":
        release_failed = [gate for gate in rubric["public_release_gates"] if gates.get(gate) is not True]
    threshold_key = "public_release" if mode == "public-release" else "candidate"
    threshold = float(rubric["thresholds"][threshold_key])
    passed = not problems and not failed_gates and not release_failed and score >= threshold
    return {
        "standard": rubric.get("name"),
        "standard_version": rubric.get("version"),
        "operating_model": rubric.get("operating_model"),
        "artifact": artifact,
        "mode": mode,
        "automation_assessed": True,
        "weighted_score": round(score, 2),
        "threshold": threshold,
        "failed_dimensions": problems,
        "failed_hard_gates": failed_gates,
        "failed_release_gates": release_failed,
        "release_authority_granted": False,
        "status": "PASS" if passed else "FAIL",
    }


def run_self_test() -> None:
    rubric = {
        "name": "self-test",
        "version": "0",
        "operating_model": "automation-first, exception-driven, human-governed",
        "thresholds": {"candidate": 90, "public_release": 92},
        "dimensions": {"a": {"weight": 0.5}, "b": {"weight": 0.5}},
        "hard_gates": ["safe"],
        "public_release_gates": ["approved"],
        "rules": {
            "maximum_safe_high_value_automation_default": True,
            "automation_must_not_reduce_quality_or_governance": True,
            "quality_pass_does_not_grant_release_authority": True
        }
    }
    validate_rubric(rubric)
    receipt = {
        "artifact": {"name": "test", "version": "1"},
        "ai_uses": [{"purpose": "test", "user_or_production_value": "test", "human_oversight": "test"}],
        "automation": {
            "assessed": True,
            "automated_stages": ["test validation"],
            "retained_human_controls": ["public release approval"],
            "no_additional_automation_rationale": "Consequential release approval remains human-governed."
        },
        "dimensions": {"a": {"score": 100, "evidence": ["ok"]}, "b": {"score": 100, "evidence": ["ok"]}},
        "gates": {"safe": True, "approved": False}
    }
    candidate = evaluate(rubric, receipt, "candidate")
    if candidate["status"] != "PASS":
        raise GateError("Self-test candidate mode should pass")
    public = evaluate(rubric, receipt, "public-release")
    if public["status"] != "FAIL" or "approved" not in public["failed_release_gates"]:
        raise GateError("Self-test public-release mode must preserve approval gate")
    missing_automation = dict(receipt)
    missing_automation.pop("automation")
    try:
        evaluate(rubric, missing_automation, "candidate")
    except GateError as exc:
        if "automation" not in str(exc).lower():
            raise GateError("Self-test automation failure produced the wrong error") from exc
    else:
        raise GateError("Self-test must reject a receipt without an automation assessment")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rubric", default="rubric.json")
    parser.add_argument("--receipt")
    parser.add_argument("--mode", choices=("candidate", "public-release"), default="candidate")
    parser.add_argument("--rubric-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.self_test:
            run_self_test()
            print("Premium AI gate self-test: PASS")
            return 0
        rubric = load_json(Path(args.rubric))
        validate_rubric(rubric)
        if args.rubric_only:
            print(f"Rubric validation: PASS ({rubric.get('name')} v{rubric.get('version')})")
            return 0
        if not args.receipt:
            raise GateError("--receipt is required unless --rubric-only or --self-test is used")
        receipt = load_json(Path(args.receipt))
        result = evaluate(rubric, receipt, args.mode)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["status"] == "PASS" else 2
    except GateError as exc:
        print(f"Premium AI gate: FAIL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
