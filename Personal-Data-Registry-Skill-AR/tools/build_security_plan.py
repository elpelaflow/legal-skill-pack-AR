#!/usr/bin/env python3
"""Generar un plan documental básico de seguridad para AAIP."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SECURITY_ITEMS = [
    "Control de acceso y permisos",
    "Autenticación y contraseñas",
    "Backups y recuperación",
    "Registro y gestión de incidentes",
    "Gestión de terceros y vendors",
    "Retención y eliminación",
    "Capacitación interna",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build(intake: dict, databases: dict) -> dict:
    return {
        "controller_name": intake.get("controller_name", ""),
        "hosting_locations": intake.get("hosting_locations", []),
        "vendors": intake.get("vendors", []),
        "sensitive_data": intake.get("sensitive_data", False),
        "items": [
            {
                "control": item,
                "status": "Pendiente relevamiento",
                "evidence": "",
                "gap": "",
                "priority": "Alta" if intake.get("sensitive_data", False) else "Media",
            }
            for item in SECURITY_ITEMS
        ],
        "databases_count": len(databases.get("databases", [])),
    }


def write_markdown(path: Path, result: dict) -> None:
    lines = [
        "# Plan de Seguridad AAIP",
        "",
        f"- Responsable: {result.get('controller_name', '')}",
        f"- Ubicaciones de hosting: {', '.join(result.get('hosting_locations', [])) or 'Pendiente'}",
        f"- Vendors: {', '.join(result.get('vendors', [])) or 'Pendiente'}",
        f"- Bases relevadas: {result.get('databases_count', 0)}",
        "",
    ]
    for item in result.get("items", []):
        lines.extend(
            [
                f"## {item['control']}",
                "",
                f"- Estado: {item['status']}",
                f"- Evidencia: {item['evidence'] or 'Pendiente'}",
                f"- Brecha: {item['gap'] or 'Pendiente'}",
                f"- Prioridad: {item['priority']}",
                "",
            ]
        )
    lines.extend(
        [
            "```text",
            "STOP_FOR_USER",
            "NEXT_ACTION: Complete el estado real de los controles y confirme vendors, hosting y brechas.",
            "```",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intake", required=True)
    parser.add_argument("--databases", required=True)
    parser.add_argument("--out-dir", default="RegistroDatosAAIP/Borradores")
    args = parser.parse_args()

    intake = load_json(Path(args.intake))
    databases = load_json(Path(args.databases))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    result = build(intake, databases)
    (out_dir / "PlanSeguridadAAIP.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(out_dir / "PlanSeguridadAAIP.md", result)
    print(f"OK plan seguridad: {out_dir / 'PlanSeguridadAAIP.md'}")
    print("STOP_FOR_USER")


if __name__ == "__main__":
    main()
