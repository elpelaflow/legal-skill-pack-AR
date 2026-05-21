#!/usr/bin/env python3
"""Preparar paquete de firma para NDA en Argentina."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build(data: dict) -> dict:
    mode = data.get("signature_mode", "")
    mode_text = str(mode).lower()
    if "digital" in mode_text:
        evidence_level = "alta"
    elif "plataforma" in mode_text or "electr" in mode_text:
        evidence_level = "media"
    else:
        evidence_level = "mayor cautela"
    return {
        "signature_mode": mode,
        "note": (
            "Verificar si el cierre previsto es con firma electrónica o con firma digital conforme a Ley 25.506."
        ),
        "platform": "Pendiente",
        "evidence_level": evidence_level,
        "recommended_checks": [
            "identificar claramente a los firmantes",
            "conservar evidencia del flujo de aceptación",
            "guardar versión final cerrada del documento",
        ],
        "confirmation_required": True,
        "user_confirmed": False,
    }


def write_md(path: Path, result: dict) -> None:
    lines = [
        "# Paquete de Firma",
        "",
        f"- Modalidad declarada: {result.get('signature_mode') or 'Pendiente'}",
        f"- Plataforma o mecanismo: {result.get('platform') or 'Pendiente'}",
        f"- Nivel de cautela probatoria: {result.get('evidence_level') or 'Pendiente'}",
        "",
        result.get("note") or "",
        "",
    ]
    lines.extend(["## Checks sugeridos", ""])
    lines.extend(f"- {item}" for item in result.get("recommended_checks", []))
    lines.extend([
        "",
        "```text",
        "STOP_FOR_USER",
        "NEXT_ACTION: Confirme si el documento se cerrará con firma electrónica o firma digital.",
        "```",
        "",
    ])
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
    (out_dir / "PaqueteFirma.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_md(out_dir / "PaqueteFirma.md", result)
    print(f"OK firma: {out_dir / 'PaqueteFirma.md'}")
    print("STOP_FOR_USER")


if __name__ == "__main__":
    main()
