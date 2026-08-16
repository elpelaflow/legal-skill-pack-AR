#!/usr/bin/env python3
"""Generar borrador del responsable para AAIP."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build(intake: dict) -> dict:
    return {
        "controller_name": intake.get("controller_name", ""),
        "controller_id": intake.get("controller_id", ""),
        "controller_address": intake.get("controller_address", ""),
        "controller_country": intake.get("controller_country", "Argentina"),
        "contact_email": intake.get("contact_email", ""),
        "business_activity": intake.get("business_activity", ""),
        "notes": intake.get("notes", ""),
        "confirmation_required": True,
        "user_confirmed": False,
    }


def write_markdown(path: Path, data: dict) -> None:
    lines = [
        "# Responsable AAIP",
        "",
        f"➤ **Responsable**: {data.get('controller_name') or 'Pendiente'}",
        f"➤ **Identificación**: {data.get('controller_id') or 'Pendiente'}",
        f"➤ **Domicilio**: {data.get('controller_address') or 'Pendiente'}",
        f"➤ **País**: {data.get('controller_country') or 'Pendiente'}",
        f"➤ **Correo**: {data.get('contact_email') or 'Pendiente'}",
        "",
        "## Actividad",
        "",
        data.get("business_activity") or "Pendiente",
        "",
        "## Observaciones",
        "",
        data.get("notes") or "Sin observaciones",
        "",
        "```text",
        "STOP_FOR_USER",
        "NEXT_ACTION: Confirme los datos del responsable antes de usarlos en trámites o registros.",
        "```",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intake", required=True)
    parser.add_argument("--out-dir", default="RegistroDatosAAIP/Borradores")
    args = parser.parse_args()

    intake = load_json(Path(args.intake))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    result = build(intake)
    (out_dir / "ResponsableAAIP.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(out_dir / "ResponsableAAIP.md", result)
    print(f"OK responsable: {out_dir / 'ResponsableAAIP.md'}")
    print("STOP_FOR_USER")


if __name__ == "__main__":
    main()
