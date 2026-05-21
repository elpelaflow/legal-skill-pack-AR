#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_guide(intake: dict, contract: dict, invoice: dict, tax: dict, fx: dict) -> str:
    lines = [
        "# Guia de factura E y cobro del exterior",
        "",
        "## Resumen del caso",
        "",
        f"- Emisor: {intake.get('taxpayer_name', 'Pendiente')}",
        f"- Regimen: {intake.get('taxpayer_regime', 'Pendiente')}",
        f"- Cliente exterior: {intake.get('client_country', contract.get('country', 'Pendiente'))}",
        f"- Moneda: {invoice.get('currency', 'Pendiente')}",
        f"- Servicio: {invoice.get('service_type', 'Pendiente')}",
        f"- Canal de cobro: {invoice.get('payment_channel', fx.get('payment_channel', 'Pendiente'))}",
        "",
        "## Como facturar",
        "",
        f"- Comprobante sugerido: clase {invoice.get('invoice_type', 'Pendiente')}",
        "- Confirmar habilitacion de punto de venta y sistema de emision en ARCA.",
        "- Validar datos del cliente exterior y descripcion del servicio.",
        "- Revisar la condicion o fecha de pago a informar segun el circuito aplicable.",
        "",
        "## Como pensar impuestos",
        "",
        "- No tratar la operacion como venta interna para cargar IVA local en la factura.",
        f"- Retencion extranjera visible en contrato: {'si' if tax.get('retencion_extranjera_visible') else 'no'}",
        "- Revisar con contador percepciones locales, tratamiento provincial y cualquier antecedente historico relevante.",
        "",
        "## Como pensar cambios",
        "",
        f"- Canal de cobro: {fx.get('payment_channel', 'Pendiente')}",
        f"- Banco / entidad: {fx.get('receiving_bank', 'Pendiente')}",
        "- Confirmar con banco o entidad el circuito documental de ingreso y liquidacion.",
        "- Si hay excepciones o canales no bancarios, validar antes de operar.",
        "",
        "## Riesgos",
        "",
        f"- Riesgo fiscal: {tax.get('risk_level', 'Pendiente')}",
        f"- Riesgo cambiario: {fx.get('risk_level', 'Pendiente')}",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intake", required=True)
    parser.add_argument("--contract", required=True)
    parser.add_argument("--invoice", required=True)
    parser.add_argument("--tax", required=True)
    parser.add_argument("--fx", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    guide = build_guide(
        load_json(Path(args.intake)),
        load_json(Path(args.contract)),
        load_json(Path(args.invoice)),
        load_json(Path(args.tax)),
        load_json(Path(args.fx)),
    )
    (out_dir / "GuiaFacturaEExportacion.md").write_text(guide, encoding="utf-8")


if __name__ == "__main__":
    main()
