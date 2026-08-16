#!/usr/bin/env python3
"""Generar matriz de propiedad intelectual para contrato de software."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build(data: dict) -> dict:
    return {
        "project_name": data.get("project_name", ""),
        "preexisting_provider_assets": [],
        "custom_deliverables": [],
        "third_party_components": [],
        "client_rights_model": data.get("ip_expectation", ""),
        "transfer_condition": "Pendiente",
        "confirmation_required": True,
        "user_confirmed": False,
    }


def write_md(path: Path, result: dict) -> None:
    lines = [
        "# Matriz de Propiedad Intelectual",
        "",
        f"- Proyecto: {result.get('project_name') or 'Pendiente'}",
        f"- Modelo esperado: {result.get('client_rights_model') or 'Pendiente'}",
        "",
        "## Código o activos preexistentes del proveedor",
        "",
        "- Pendiente",
        "",
        "## Entregables a medida",
        "",
        "- Pendiente",
        "",
        "## Componentes de terceros / Open Source",
        "",
        "- Pendiente",
        "",
        "## Condición de transferencia o licencia",
        "",
        f"- {result.get('transfer_condition') or 'Pendiente'}",
        "",
        "```text",
        "STOP_FOR_USER",
        "NEXT_ACTION: Confirme cesión, licencia, reservas y terceros antes del borrador contractual.",
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
    (out_dir / "MatrizPI.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_md(out_dir / "MatrizPI.md", result)
    print(f"OK PI: {out_dir / 'MatrizPI.md'}")
    print("STOP_FOR_USER")


if __name__ == "__main__":
    main()
