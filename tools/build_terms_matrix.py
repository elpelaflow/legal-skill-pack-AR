#!/usr/bin/env python3
"""Generar matriz de términos y condiciones."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build(data: dict) -> dict:
    clauses_required = []
    if data.get("user_accounts", False):
        clauses_required.extend(["cuentas", "credenciales", "suspensión"])
    if data.get("payments", False):
        clauses_required.extend(["pagos", "suscripciones o cobros", "cancelación"])
    if data.get("ads_monetization", False):
        clauses_required.append("publicidad")
    tracker_text = " ".join(str(item).lower() for item in data.get("cookies_or_trackers", []))
    if any(word in tracker_text for word in ["remarketing", "pixel", "ads"]):
        clauses_required.append("interacción con publicidad y tracking")
    return {
        "service_name": data.get("service_name", ""),
        "user_accounts": bool(data.get("user_accounts", False)),
        "payments": bool(data.get("payments", False)),
        "ads": bool(data.get("ads_monetization", False)),
        "clauses_required": clauses_required,
        "confirmation_required": True,
        "user_confirmed": False,
    }


def write_md(path: Path, result: dict) -> None:
    lines = [
        "# Matriz de Términos y Condiciones",
        "",
        f"- Servicio: {result.get('service_name') or 'Pendiente'}",
        f"- Cuentas: {'Sí' if result.get('user_accounts') else 'No'}",
        f"- Pagos: {'Sí' if result.get('payments') else 'No'}",
        f"- Anuncios: {'Sí' if result.get('ads') else 'No'}",
        "",
    ]
    lines.extend(["## Cláusulas requeridas", ""])
    if result.get("clauses_required"):
        lines.extend(f"- {item}" for item in result["clauses_required"])
    else:
        lines.append("- Pendiente")
    lines.extend([
        "",
        "```text",
        "STOP_FOR_USER",
        "NEXT_ACTION: Confirme reglas de uso, cuentas, pagos y baja antes del borrador final.",
        "```",
        "",
    ])
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
    (out_dir / "MatrizTerminos.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_md(out_dir / "MatrizTerminos.md", result)
    print(f"OK términos: {out_dir / 'MatrizTerminos.md'}")
    print("STOP_FOR_USER")


if __name__ == "__main__":
    main()
