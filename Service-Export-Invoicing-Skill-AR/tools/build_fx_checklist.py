#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_fx_checklist(intake: dict, contract: dict, tax: dict) -> dict:
    payment_channel = intake.get("payment_channel", "Pendiente")
    if payment_channel == "Pendiente":
        payment_channel = contract.get("payment_channel_hint", "Pendiente")
    bank = intake.get("receiving_bank", "Pendiente")
    risk = (
        "alto"
        if contract.get("mentions_crypto", False) or payment_channel in {"wallet_cripto", "Pendiente"}
        else "medio"
        if bank == "Pendiente" or payment_channel == "plataforma_cobro"
        else tax.get("risk_level", "medio")
    )

    items = [
        "Confirmar canal de cobro y titularidad de la cuenta receptora.",
        "Conservar contrato, propuesta, orden de compra o soporte equivalente.",
        "Conservar factura E emitida y constancias del cobro.",
        "Consultar al banco o entidad interviniente la documentacion requerida para ingreso de fondos.",
        "Verificar si corresponde liquidacion obligatoria o si el caso requiere revisar una excepcion especifica.",
    ]
    if payment_channel == "plataforma_cobro":
        items.append("Revisar trazabilidad entre plataforma, titularidad de fondos y liquidacion final.")
    if bank == "Pendiente":
        items.append("Definir banco o entidad local antes de operar.")
    if contract.get("mentions_crypto", False) or payment_channel == "wallet_cripto":
        items.append("Caso con cripto: no operar sin validacion profesional previa.")

    return {
        "payment_channel": payment_channel,
        "receiving_bank": bank,
        "risk_level": risk,
        "items": items,
    }


def write_markdown(data: dict, out_path: Path) -> None:
    lines = [
        "# Checklist cambiario de exportacion",
        "",
        f"- Canal de cobro: {data['payment_channel']}",
        f"- Banco / entidad receptora: {data['receiving_bank']}",
        f"- Riesgo: {data['risk_level']}",
        "",
        "## Tareas",
        "",
    ]
    for item in data["items"]:
        lines.append(f"- {item}")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intake", required=True)
    parser.add_argument("--contract", required=True)
    parser.add_argument("--tax", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    data = build_fx_checklist(
        load_json(Path(args.intake)),
        load_json(Path(args.contract)),
        load_json(Path(args.tax)),
    )
    (out_dir / "ChecklistCambiosExportacion.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    write_markdown(data, out_dir / "ChecklistCambiosExportacion.md")


if __name__ == "__main__":
    main()
