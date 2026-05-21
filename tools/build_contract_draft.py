#!/usr/bin/env python3
"""Consolidar borrador contractual de desarrollo de software."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_md(path: Path, intake: dict, scope: dict, payment: dict, ip: dict) -> None:
    lines = [
        "# Contrato de Desarrollo de Software (Borrador)",
        "",
        f"➤ **Cliente**: {intake.get('client_name') or 'Pendiente'}",
        f"➤ **Proveedor**: {intake.get('provider_name') or 'Pendiente'}",
        f"➤ **Proyecto**: {intake.get('project_name') or 'Pendiente'}",
        f"➤ **Modalidad**: {intake.get('engagement_model') or 'Pendiente'}",
        "",
        "## 1. Objeto",
        "",
        intake.get("project_summary") or "Pendiente",
        "",
        "## 2. Alcance",
        "",
        "- Ver Matriz de Alcance confirmada.",
        "",
        "## 3. Entregables y Aceptación",
        "",
        "- Los entregables, hitos y criterios de aceptación deberán surgir de la matriz confirmada por las partes.",
        "",
        "## 4. Precio y Pagos",
        "",
        f"- Modelo económico: {payment.get('payment_model') or 'Pendiente'}",
        f"- Moneda: {payment.get('currency') or 'Pendiente'}",
        "",
        "## 5. Propiedad Intelectual",
        "",
        f"- Modelo de derechos esperado: {ip.get('client_rights_model') or 'Pendiente'}",
        f"- Condición de transferencia/licencia: {ip.get('transfer_condition') or 'Pendiente'}",
        "",
        "## 6. Confidencialidad",
        "",
        "- Las partes deberán mantener reserva sobre la información confidencial intercambiada con motivo del proyecto.",
        "",
        "## 7. Garantía y Soporte",
        "",
        "- Debe distinguirse entre corrección de errores incluidos y soporte posterior adicional.",
        "",
        "## 8. Terminación",
        "",
        "- Deben precisarse causales de terminación y efectos sobre pagos y entregables.",
        "",
        "## 9. Ley y Jurisdicción",
        "",
        "- Pendiente confirmar.",
        "",
        "```text",
        "STOP_FOR_USER",
        "NEXT_ACTION: Revise el borrador completo y confirme antes de usarlo en negociación o firma.",
        "```",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intake", required=True)
    parser.add_argument("--scope", required=True)
    parser.add_argument("--payment", required=True)
    parser.add_argument("--ip", required=True)
    parser.add_argument("--out-dir", default="ContratoDesarrolloSoftware/Borradores")
    args = parser.parse_args()

    intake = load_json(Path(args.intake))
    scope = load_json(Path(args.scope))
    payment = load_json(Path(args.payment))
    ip = load_json(Path(args.ip))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    write_md(out_dir / "ContratoDesarrolloSoftware.md", intake, scope, payment, ip)
    print(f"OK contrato: {out_dir / 'ContratoDesarrolloSoftware.md'}")
    print("STOP_FOR_USER")


if __name__ == "__main__":
    main()
