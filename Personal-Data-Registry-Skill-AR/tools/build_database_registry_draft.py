#!/usr/bin/env python3
"""Generar fichas por base de datos para revisión registral."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def safe_name(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9_-]+", "_", value.strip())
    return value.strip("_") or "BASE"


def write_base_md(path: Path, base: dict, controller_name: str) -> None:
    lines = [
        f"# {base.get('name', 'Base de Datos')}",
        "",
        f"➤ **Responsable**: {controller_name or 'Pendiente'}",
        f"➤ **Finalidad**: {base.get('purpose') or 'Pendiente'}",
        f"➤ **Titulares**: {', '.join(base.get('data_subjects', [])) or 'Pendiente'}",
        f"➤ **Categorías de datos**: {', '.join(base.get('data_categories', [])) or 'Pendiente'}",
        f"➤ **Datos sensibles**: {'Sí' if base.get('sensitive_data') else 'No'}",
        f"➤ **Terceros**: {', '.join(base.get('third_parties', [])) or 'No informado'}",
        f"➤ **Transferencia internacional**: {'Sí' if base.get('international_transfer') else 'No'}",
        f"➤ **Conservación**: {base.get('retention_criteria') or 'Pendiente'}",
        f"➤ **Riesgo**: {base.get('risk_level') or 'Pendiente'}",
        "",
        "## Observaciones",
        "",
        base.get("notes") or "Sin observaciones",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intake", required=True)
    parser.add_argument("--databases", required=True)
    parser.add_argument("--out-dir", default="RegistroDatosAAIP/Borradores")
    args = parser.parse_args()

    intake = load_json(Path(args.intake))
    data = load_json(Path(args.databases))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    index = {
        "controller_name": intake.get("controller_name", ""),
        "files": [],
        "risk_summary": [],
    }
    for base in data.get("databases", []):
        if not base.get("selected", True):
            continue
        filename = f"Base_{safe_name(base.get('name', 'BASE'))}.md"
        write_base_md(out_dir / filename, base, intake.get("controller_name", ""))
        index["files"].append(filename)
        index["risk_summary"].append(
            {
                "name": base.get("name", ""),
                "risk_level": base.get("risk_level", "pendiente"),
                "sensitive_data": bool(base.get("sensitive_data")),
                "international_transfer": bool(base.get("international_transfer")),
            }
        )

    (out_dir / "BasesRegistro.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK fichas por base: {len(index['files'])}")


if __name__ == "__main__":
    main()
