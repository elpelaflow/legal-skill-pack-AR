#!/usr/bin/env python3
"""Generar matriz de confidencialidad para NDA."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build(data: dict) -> dict:
    assets = [str(item) for item in data.get("confidential_assets", [])]
    joined = " ".join(item.lower() for item in assets)
    categories = []
    if any(word in joined for word in ["codigo", "código", "repo", "arquitect", "documentacion", "documentación"]):
        categories.append("tecnica")
    if any(word in joined for word in ["pricing", "cliente", "roadmap", "propuesta", "comercial"]):
        categories.append("comercial")
    if any(word in joined for word in ["credencial", "acceso", "password", "token", "ambiente"]):
        categories.append("operativa")
    if any(word in joined for word in ["dato", "dataset", "base", "personal", "regulado"]):
        categories.append("datos")
    regulated = any(word in joined for word in ["dato personal", "datos personales", "salud", "financier", "regulado", "dataset"])
    return {
        "nda_type": data.get("nda_type", ""),
        "purpose": data.get("purpose", ""),
        "confidential_assets": assets,
        "asset_categories": categories,
        "exclusions": [
            "información pública",
            "información ya conocida legítimamente",
            "información recibida legítimamente de terceros sin deber de reserva",
            "información desarrollada independientemente",
        ],
        "term_summary": data.get("term_summary", ""),
        "need_to_know_sharing": ["empleados", "asesores", "contratistas"],
        "regulated_or_personal_data": regulated,
        "risk_level": "alto" if regulated or "operativa" in categories else ("medio" if "tecnica" in categories or "comercial" in categories else "bajo"),
        "confirmation_required": True,
        "user_confirmed": False,
    }


def write_md(path: Path, result: dict) -> None:
    lines = [
        "# Matriz de Confidencialidad",
        "",
        f"- Tipo de NDA: {result.get('nda_type') or 'Pendiente'}",
        f"- Propósito: {result.get('purpose') or 'Pendiente'}",
        f"- Activos confidenciales: {result.get('confidential_assets') or 'Pendiente'}",
        f"- Categorías detectadas: {result.get('asset_categories') or 'Pendiente'}",
        f"- Datos personales o regulados: {'Sí' if result.get('regulated_or_personal_data') else 'No'}",
        f"- Riesgo: {result.get('risk_level') or 'Pendiente'}",
        "",
        "## Exclusiones sugeridas",
        "",
    ]
    lines.extend(f"- {item}" for item in result.get("exclusions", []))
    lines.extend(["", "## Sharing controlado sugerido", ""])
    lines.extend(f"- {item}" for item in result.get("need_to_know_sharing", []))
    lines.extend(
        [
            "",
            "## Plazo",
            "",
            f"- {result.get('term_summary') or 'Pendiente'}",
            "",
            "```text",
            "STOP_FOR_USER",
            "NEXT_ACTION: Confirme alcance confidencial, exclusiones y plazo antes del borrador final.",
            "```",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out-dir", default="AcuerdoConfidencialidad/Borradores")
    args = parser.parse_args()
    data = load_json(Path(args.input))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    result = build(data)
    (out_dir / "MatrizConfidencialidad.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_md(out_dir / "MatrizConfidencialidad.md", result)
    print(f"OK matriz confidencialidad: {out_dir / 'MatrizConfidencialidad.md'}")
    print("STOP_FOR_USER")


if __name__ == "__main__":
    main()
