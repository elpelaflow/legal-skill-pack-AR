#!/usr/bin/env python3
"""Generar esquema base de pagos para contrato de desarrollo."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build(data: dict) -> dict:
    model = data.get("payment_model", "")
    return {
        "project_name": data.get("project_name", ""),
        "payment_model": model,
        "currency": "Pendiente",
        "schedule": [],
        "late_payment_rule": "Pendiente",
        "tax_rule": "Pendiente",
        "confirmation_required": True,
        "user_confirmed": False,
    }


def write_md(path: Path, result: dict) -> None:
    lines = [
        "# Esquema de Pagos",
        "",
        f"- Proyecto: {result.get('project_name') or 'Pendiente'}",
        f"- Modelo: {result.get('payment_model') or 'Pendiente'}",
        f"- Moneda: {result.get('currency') or 'Pendiente'}",
        "",
        "## Hitos / Vencimientos",
        "",
        "- Pendiente",
        "",
        "## Mora",
        "",
        f"- {result.get('late_payment_rule') or 'Pendiente'}",
        "",
        "## Impuestos",
        "",
        f"- {result.get('tax_rule') or 'Pendiente'}",
        "",
        "```text",
        "STOP_FOR_USER",
        "NEXT_ACTION: Confirme modelo económico, hitos, moneda, impuestos y mora.",
        "```",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out-dir", default="ContratoDesarrolloSoftware/Borradores")
    args = parser.parse_args()
    data = load_json(Path(args.input))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    result = build(data)
    (out_dir / "EsquemaPagos.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_md(out_dir / "EsquemaPagos.md", result)
    print(f"OK pagos: {out_dir / 'EsquemaPagos.md'}")
    print("STOP_FOR_USER")


if __name__ == "__main__":
    main()
