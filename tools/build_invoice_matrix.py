#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_matrix(intake: dict, contract: dict) -> dict:
    client_country = intake.get("client_country", "Pendiente")
    if client_country == "Pendiente":
        client_country = contract.get("country", "Pendiente")
    currency = intake.get("invoice_currency", "Pendiente")
    if currency == "Pendiente":
        currency = contract.get("currency", "Pendiente")
    payment_channel = intake.get("payment_channel", "Pendiente")
    if payment_channel == "Pendiente":
        payment_channel = contract.get("payment_channel_hint", "Pendiente")

    return {
        "invoice_type": "E",
        "taxpayer_regime": intake.get("taxpayer_regime", "Pendiente"),
        "client_country": client_country,
        "currency": currency,
        "service_type": contract.get("service_type", intake.get("service_type", "Pendiente")),
        "service_matches": contract.get("service_matches", []),
        "payment_channel": payment_channel,
        "payment_terms": contract.get("payment_terms", "Pendiente"),
        "required_checks": [
            "Confirmar habilitacion de comprobantes clase E en ARCA.",
            "Confirmar punto de venta y sistema de emision.",
            "Confirmar identificacion del cliente exterior.",
            "Confirmar descripcion suficiente del servicio exportado.",
            "Confirmar fecha o condicion de pago a informar segun el circuito aplicable.",
        ],
        "risk_flags": [
            flag for flag, active in {
                "retencion_extranjera_visible": contract.get("mentions_foreign_tax", False),
                "gastos_reembolsables": contract.get("mentions_reimbursements", False),
                "cripto": contract.get("mentions_crypto", False),
                "canal_no_bancario_claro": payment_channel in {"plataforma_cobro", "wallet_cripto", "Pendiente"},
                "servicio_mixto": len(contract.get("service_matches", [])) > 1,
            }.items() if active
        ],
    }


def write_markdown(data: dict, out_path: Path) -> None:
    lines = [
        "# Matriz de factura E",
        "",
        f"- Tipo de comprobante: {data['invoice_type']}",
        f"- Regimen del emisor: {data['taxpayer_regime']}",
        f"- Pais del cliente: {data['client_country']}",
        f"- Moneda: {data['currency']}",
        f"- Servicio: {data['service_type']}",
        f"- Canal de cobro: {data['payment_channel']}",
        f"- Termino de pago: {data['payment_terms']}",
        "",
        "## Validaciones operativas",
        "",
    ]
    for item in data["required_checks"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Flags de riesgo", ""])
    for flag in data["risk_flags"] or ["sin_flags_detectados"]:
        lines.append(f"- {flag}")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intake", required=True)
    parser.add_argument("--contract", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    data = build_matrix(load_json(Path(args.intake)), load_json(Path(args.contract)))
    (out_dir / "MatrizFacturaE.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    write_markdown(data, out_dir / "MatrizFacturaE.md")


if __name__ == "__main__":
    main()
