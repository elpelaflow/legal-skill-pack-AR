#!/usr/bin/env python3
"""Generar matriz de lógica legal para smart contracts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build(data: dict) -> dict:
    return {
        "project_name": data.get("project_name", ""),
        "business_purpose": data.get("business_purpose", ""),
        "automated_action": data.get("automated_action", ""),
        "conditions": [],
        "exceptions": [],
        "offchain_remedies": [],
        "confirmation_required": True,
        "user_confirmed": False,
    }


def write_md(path: Path, result: dict) -> None:
    lines = [
        "# Matriz de Lógica Legal",
        "",
        f"- Proyecto: {result.get('project_name') or 'Pendiente'}",
        f"- Propósito: {result.get('business_purpose') or 'Pendiente'}",
        f"- Acción automatizada: {result.get('automated_action') or 'Pendiente'}",
        "",
        "## Condiciones",
        "",
        "- Pendiente",
        "",
        "## Excepciones",
        "",
        "- Pendiente",
        "",
        "## Remedios fuera de cadena",
        "",
        "- Pendiente",
        "",
        "```text",
        "STOP_FOR_USER",
        "NEXT_ACTION: Confirme condiciones, excepciones y remedios antes de seguir.",
        "```",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out-dir", default="SmartContractSpecAR/Borradores")
    args = parser.parse_args()
    data = load_json(Path(args.input))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    result = build(data)
    (out_dir / "MatrizLogicaLegal.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_md(out_dir / "MatrizLogicaLegal.md", result)
    print(f"OK lógica legal: {out_dir / 'MatrizLogicaLegal.md'}")
    print("STOP_FOR_USER")


if __name__ == "__main__":
    main()
