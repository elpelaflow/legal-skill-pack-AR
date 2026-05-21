#!/usr/bin/env python3
"""Generar checklist de inspección y madurez AAIP."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def maturity_level(intake: dict, databases: dict, security: dict) -> str:
    has_controller = bool(intake.get("controller_name") and intake.get("controller_id"))
    has_databases = bool(databases.get("databases"))
    security_items = security.get("items", [])
    has_security = bool(security_items)
    has_transfers = bool(intake.get("vendors") or intake.get("hosting_locations"))
    if has_controller and has_databases and has_security and has_transfers:
        return "media"
    if has_controller and has_databases:
        return "baja-media"
    return "baja"


def overall_risk(databases: dict, intake: dict) -> str:
    if intake.get("sensitive_data") or any(item.get("risk_level") == "alto" for item in databases.get("databases", [])):
        return "alto"
    if any(item.get("risk_level") == "medio" for item in databases.get("databases", [])):
        return "medio"
    return "bajo"


def write_markdown(path: Path, intake: dict, databases: dict, security: dict) -> None:
    maturity = maturity_level(intake, databases, security)
    risk = overall_risk(databases, intake)
    lines = [
        "# Checklist de Inspección AAIP",
        "",
        f"- Responsable: {intake.get('controller_name') or 'Pendiente'}",
        f"- Nivel de madurez documental: {maturity}",
        f"- Riesgo global estimado: {risk}",
        "",
        "## Checklist",
        "",
        f"- Responsable identificado: {'Sí' if intake.get('controller_name') else 'No'}",
        f"- Identificación del responsable: {'Sí' if intake.get('controller_id') else 'No'}",
        f"- Bases detectadas: {'Sí' if databases.get('databases') else 'No'}",
        f"- Vendors relevados: {'Sí' if intake.get('vendors') else 'No'}",
        f"- Hosting relevado: {'Sí' if intake.get('hosting_locations') else 'No'}",
        f"- Plan de seguridad: {'Sí' if security.get('items') else 'No'}",
        f"- Datos sensibles declarados: {'Sí' if intake.get('sensitive_data') else 'No'}",
        "",
        "## Riesgo por base",
        "",
    ]
    for item in databases.get("databases", []):
        lines.append(
            f"- {item.get('name', 'Base')}: riesgo {item.get('risk_level', 'pendiente')}, "
            f"sensibles={'sí' if item.get('sensitive_data') else 'no'}, "
            f"transferencia={'sí' if item.get('international_transfer') else 'no'}"
        )
    lines.extend(
        [
            "",
            "## Brechas típicas a completar",
            "",
            "- Finalidad específica por base.",
            "- Plazo o criterio de conservación por base.",
            "- Terceros con acceso operativo real.",
            "- Confirmación de transferencias internacionales.",
            "- Estado real de controles de seguridad.",
            "",
            "```text",
            "STOP_FOR_USER",
            "NEXT_ACTION: Revise el nivel de madurez, riesgo por base y brechas pendientes antes de usar la documentación en una revisión formal.",
            "```",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intake", required=True)
    parser.add_argument("--databases", required=True)
    parser.add_argument("--security", required=True)
    parser.add_argument("--out-dir", default="RegistroDatosAAIP/Borradores")
    args = parser.parse_args()

    intake = load_json(Path(args.intake))
    databases = load_json(Path(args.databases))
    security = load_json(Path(args.security))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    write_markdown(out_dir / "ChecklistInspeccionAAIP.md", intake, databases, security)
    print(f"OK checklist: {out_dir / 'ChecklistInspeccionAAIP.md'}")
    print("STOP_FOR_USER")


if __name__ == "__main__":
    main()
