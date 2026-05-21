#!/usr/bin/env python3
"""Generar procedimiento básico para derechos del titular."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_markdown(path: Path, intake: dict) -> None:
    lines = [
        "# Procedimiento de Derechos del Titular",
        "",
        f"- Responsable: {intake.get('controller_name') or 'Pendiente'}",
        f"- Canal sugerido: {intake.get('contact_email') or 'Pendiente'}",
        "",
        "## Flujo sugerido",
        "",
        "1. Recepción del pedido por canal designado.",
        "2. Verificación razonable de identidad.",
        "3. Registro interno del caso.",
        "4. Derivación al área responsable.",
        "5. Búsqueda en bases involucradas.",
        "6. Respuesta, rectificación, actualización o supresión según corresponda.",
        "7. Cierre y archivo de evidencia.",
        "",
        "## Controles mínimos",
        "",
        "- Mantener trazabilidad del pedido.",
        "- No responder sin validar identidad.",
        "- Coordinar con terceros si la información está replicada o externalizada.",
        "- Registrar tiempos y decisión final.",
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
    write_markdown(out_dir / "ProcedimientoDerechosTitular.md", intake)
    print(f"OK procedimiento: {out_dir / 'ProcedimientoDerechosTitular.md'}")


if __name__ == "__main__":
    main()
