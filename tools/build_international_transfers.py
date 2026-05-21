#!/usr/bin/env python3
"""Generar borrador de transferencias internacionales y terceros."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_markdown(path: Path, intake: dict, databases: dict) -> None:
    hosting = intake.get("hosting_locations", [])
    vendors = intake.get("vendors", [])
    lines = [
        "# Transferencias Internacionales y Terceros",
        "",
        f"- Responsable: {intake.get('controller_name') or 'Pendiente'}",
        f"- Hosting declarado: {', '.join(hosting) or 'Pendiente'}",
        f"- Vendors declarados: {', '.join(vendors) or 'Pendiente'}",
        "",
        "## Señales a revisar",
        "",
        f"- Infraestructura fuera de Argentina: {'Sí' if any(str(item).lower() != 'argentina' for item in hosting) else 'No / Pendiente'}",
        f"- Vendors con acceso potencial a datos: {'Sí' if vendors else 'Pendiente'}",
        "",
        "## Bases alcanzadas",
        "",
    ]
    for base in databases.get("databases", []):
        lines.extend(
            [
                f"### {base.get('name', 'Base')}",
                "",
                f"- Transferencia internacional: {'Sí' if base.get('international_transfer') else 'No / Pendiente'}",
                f"- Terceros: {', '.join(base.get('third_parties', [])) or 'Pendiente'}",
                "",
            ]
        )
    lines.extend(
        [
            "## Observaciones",
            "",
            "- Confirmar si los proveedores almacenan o acceden a datos personales fuera de Argentina.",
            "- Confirmar soporte remoto, replicación, backups y subprocesadores.",
            "",
            "```text",
            "STOP_FOR_USER",
            "NEXT_ACTION: Confirme hosting, vendors, terceros con acceso y alcance de transferencias internacionales.",
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
    write_markdown(out_dir / "TransferenciasInternacionales.md", intake, databases)
    print(f"OK transferencias: {out_dir / 'TransferenciasInternacionales.md'}")
    print("STOP_FOR_USER")


if __name__ == "__main__":
    main()
