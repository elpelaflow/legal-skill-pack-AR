#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_tax_matrix(intake: dict, contract: dict, invoice: dict) -> dict:
    service_type = invoice.get("service_type", "Pendiente")
    has_foreign_withholding = contract.get("mentions_foreign_tax", False)
    taxpayer_regime = str(intake.get("taxpayer_regime", "Pendiente")).lower()
    payment_channel = invoice.get("payment_channel", "Pendiente")
    service_matches = invoice.get("service_matches", [])
    high_risk = (
        contract.get("mentions_crypto", False)
        or service_type == "Pendiente"
        or payment_channel == "wallet_cripto"
    )
    medium_risk = (
        has_foreign_withholding
        or contract.get("mentions_reimbursements", False)
        or payment_channel == "plataforma_cobro"
        or "monotrib" in taxpayer_regime
        or service_type in {"saas_licencia", "consulting_it"}
        or len(service_matches) > 1
    )

    notes = [
        "Usar comprobante clase E para documentar la operacion.",
        "No cargar IVA local como venta interna en la factura.",
        "Verificar retencion o impuesto extranjero si el contrato lo menciona.",
        "Revisar percepciones locales bancarias o provinciales por fuera del contrato.",
        "Revisar derechos de exportacion historicos solo si el periodo analizado o un plan pendiente lo vuelve relevante.",
    ]
    if high_risk:
        notes.append("Caso con riesgo alto: validar con contador antes de emitir o cobrar.")
    elif medium_risk:
        notes.append("Caso con riesgo medio: validar descripcion del servicio, retenciones y circuito de cobro.")

    return {
        "invoice_type": invoice.get("invoice_type", "E"),
        "service_type": service_type,
        "service_matches": service_matches,
        "taxpayer_regime": taxpayer_regime,
        "payment_channel": payment_channel,
        "aplica_factura_e": True,
        "no_cargar_iva_local_como_venta_interna": True,
        "retencion_extranjera_visible": has_foreign_withholding,
        "revisar_derechos_historicos_si_aplica": True,
        "revisar_percepciones_locales_fuera_del_contrato": True,
        "risk_level": "alto" if high_risk else "medio" if medium_risk else "bajo",
        "notes": notes,
    }


def write_markdown(data: dict, out_path: Path) -> None:
    lines = [
        "# Matriz fiscal de exportacion",
        "",
        f"- Comprobante: {data['invoice_type']}",
        f"- Servicio: {data['service_type']}",
        f"- Servicios detectados: {', '.join(data['service_matches']) if data['service_matches'] else data['service_type']}",
        f"- Regimen del emisor: {data['taxpayer_regime']}",
        f"- Canal de cobro: {data['payment_channel']}",
        f"- Aplica factura E: {'si' if data['aplica_factura_e'] else 'no'}",
        f"- No cargar IVA local como venta interna: {'si' if data['no_cargar_iva_local_como_venta_interna'] else 'no'}",
        f"- Retencion extranjera visible: {'si' if data['retencion_extranjera_visible'] else 'no'}",
        f"- Revisar derechos historicos si aplica: {'si' if data['revisar_derechos_historicos_si_aplica'] else 'no'}",
        f"- Revisar percepciones locales fuera del contrato: {'si' if data['revisar_percepciones_locales_fuera_del_contrato'] else 'no'}",
        f"- Riesgo: {data['risk_level']}",
        "",
        "## Notas",
        "",
    ]
    for note in data["notes"]:
        lines.append(f"- {note}")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intake", required=True)
    parser.add_argument("--contract", required=True)
    parser.add_argument("--invoice", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    data = build_tax_matrix(
        load_json(Path(args.intake)),
        load_json(Path(args.contract)),
        load_json(Path(args.invoice)),
    )
    (out_dir / "MatrizFiscalExportacion.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    write_markdown(data, out_dir / "MatrizFiscalExportacion.md")


if __name__ == "__main__":
    main()
