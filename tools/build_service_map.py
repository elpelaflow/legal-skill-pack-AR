#!/usr/bin/env python3
"""Generar mapa de servicio para documentos legales de app."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build(data: dict) -> dict:
    return {
        "service_name": data.get("service_name", ""),
        "platforms": data.get("platforms", []),
        "modules": [],
        "monetization": {
            "payments": bool(data.get("payments", False)),
            "ads": bool(data.get("ads_monetization", False)),
        },
        "confirmation_required": True,
        "user_confirmed": False,
    }


def write_md(path: Path, result: dict) -> None:
    lines = [
        "# Mapa del Servicio",
        "",
        f"- Servicio: {result.get('service_name') or 'Pendiente'}",
        f"- Plataformas: {', '.join(result.get('platforms', [])) or 'Pendiente'}",
        "",
        "## Módulos",
        "",
        "- Pendiente",
        "",
        "## Monetización",
        "",
        f"- Pagos: {'Sí' if result.get('monetization', {}).get('payments') else 'No'}",
        f"- Anuncios: {'Sí' if result.get('monetization', {}).get('ads') else 'No'}",
        "",
        "```text",
        "STOP_FOR_USER",
        "NEXT_ACTION: Confirme el mapa del producto y su monetización antes de seguir.",
        "```",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out-dir", default="LegalesAppAR/Borradores")
    args = parser.parse_args()
    data = load_json(Path(args.input))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    result = build(data)
    (out_dir / "MapaServicio.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_md(out_dir / "MapaServicio.md", result)
    print(f"OK mapa servicio: {out_dir / 'MapaServicio.md'}")
    print("STOP_FOR_USER")


if __name__ == "__main__":
    main()
