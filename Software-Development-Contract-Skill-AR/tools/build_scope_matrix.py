#!/usr/bin/env python3
"""Generar matriz de alcance para contrato de desarrollo."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build(data: dict) -> dict:
    return {
        "project_name": data.get("project_name", ""),
        "scope_items": [],
        "deliverables": [],
        "exclusions": [],
        "client_dependencies": [],
        "assumptions": [],
        "confirmation_required": True,
        "user_confirmed": False,
    }


def write_md(path: Path, result: dict) -> None:
    lines = [
        "# Matriz de Alcance",
        "",
        f"- Proyecto: {result.get('project_name') or 'Pendiente'}",
        "",
        "## Alcance",
        "",
        "- Pendiente",
        "",
        "## Entregables",
        "",
        "- Pendiente",
        "",
        "## Exclusiones",
        "",
        "- Pendiente",
        "",
        "## Dependencias del Cliente",
        "",
        "- Pendiente",
        "",
        "```text",
        "STOP_FOR_USER",
        "NEXT_ACTION: Confirme alcance, entregables, exclusiones y dependencias antes de seguir.",
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
    (out_dir / "MatrizAlcance.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_md(out_dir / "MatrizAlcance.md", result)
    print(f"OK alcance: {out_dir / 'MatrizAlcance.md'}")
    print("STOP_FOR_USER")


if __name__ == "__main__":
    main()
