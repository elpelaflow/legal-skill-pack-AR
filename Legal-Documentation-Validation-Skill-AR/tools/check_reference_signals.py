#!/usr/bin/env python3
"""Consolidar señales de referencias y contexto argentino."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


CONTEXT_EXPECTATIONS = {
    "general": [],
    "aaip": ["aaip", "ley 25.326"],
    "inpi": ["inpi"],
    "dnda": ["dnda", "ley 11.723"],
    "arca": ["arca"],
    "bcra": ["bcra"],
    "privacidad": ["aaip", "ley 25.326"],
    "firma": ["ley 25.506"],
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def merge_counts(files: list[dict], key: str) -> dict[str, int]:
    totals: dict[str, int] = {}
    for item in files:
        for name, count in item.get(key, {}).items():
            totals[name] = totals.get(name, 0) + count
    return totals


def build_issues(expected_context: str, argentina: dict[str, int], foreign: dict[str, int]) -> list[str]:
    issues: list[str] = []
    if foreign:
        issues.append("Se detectaron referencias o señales extranjeras que requieren contexto o limpieza.")
    expected = CONTEXT_EXPECTATIONS.get(expected_context, [])
    missing = [item for item in expected if item not in argentina]
    if missing:
        issues.append(f"Faltan señales esperables para el contexto '{expected_context}': {', '.join(missing)}.")
    if not argentina:
        issues.append("No se detectaron señales argentinas expresas en los documentos analizados.")
    return issues


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", required=True)
    parser.add_argument("--expected-context", default="general")
    parser.add_argument("--out-dir", default="ValidacionLegalAR/Borradores")
    args = parser.parse_args()

    inventory = load_json(Path(args.inventory))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    files = inventory.get("files", [])
    foreign = merge_counts(files, "foreign_signals")
    argentina = merge_counts(files, "argentina_signals")
    issues = build_issues(args.expected_context, argentina, foreign)

    status = "ok"
    if issues:
        status = "revisar"
    if foreign and any(name in foreign for name in ("rgpd", "gdpr", "cnipa", "delaware law")):
        status = "critico"

    payload = {
        "expected_context": args.expected_context,
        "status": status,
        "argentina_signals": argentina,
        "foreign_signals": foreign,
        "issues": issues,
    }
    (out_dir / "SenalesReferencia.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"OK referencias: {out_dir / 'SenalesReferencia.json'}")


if __name__ == "__main__":
    main()
