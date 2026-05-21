#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

COUNTRY_RULES = {
    "usa": ["united states", "usa", "u.s.", "delaware", "california", "new york"],
    "uruguay": ["uruguay", "montevideo"],
    "espana": ["spain", "españa", "madrid", "barcelona"],
    "chile": ["chile", "santiago"],
    "mexico": ["mexico", "ciudad de mexico", "cdmx"],
    "colombia": ["colombia", "bogota", "bogotá"],
}

CURRENCY_RULES = {
    "USD": ["usd", "dollar", "us$"],
    "EUR": ["eur", "euro"],
    "ARS": ["ars", "peso argentino"],
}

SERVICE_RULES = {
    "desarrollo_software": ["development", "software development", "custom software", "build feature"],
    "mantenimiento_soporte": ["support", "maintenance", "bugfix", "sla"],
    "consulting_it": ["consulting", "advisory", "architecture review"],
    "saas_licencia": ["subscription", "license", "access", "saas", "licensed access"],
}

PAYMENT_CHANNEL_RULES = {
    "banco_local": ["wire transfer", "bank transfer", "swift", "transferencia bancaria"],
    "plataforma_cobro": ["paypal", "payoneer", "stripe", "deel", "wise", "airtm"],
    "wallet_cripto": ["crypto", "usdt", "bitcoin", "wallet"],
}


def detect_first(content: str, rules: dict, default: str = "Pendiente") -> str:
    for label, needles in rules.items():
        if any(needle in content for needle in needles):
            return label
    return default


def detect_all(content: str, rules: dict) -> list[str]:
    matches = []
    for label, needles in rules.items():
        if any(needle in content for needle in needles):
            matches.append(label)
    return matches


def extract_payment_terms(content: str) -> str:
    match = re.search(r"net\s+(\d+)", content)
    if match:
        return f"net {match.group(1)}"
    if "advance" in content or "upfront" in content:
        return "adelantado"
    if "upon acceptance" in content:
        return "contra aceptacion"
    return "Pendiente"


def parse_contract(path: Path) -> dict:
    content = path.read_text(encoding="utf-8", errors="ignore").lower()
    mentions_foreign_tax = (
        ("withholding tax" in content or "tax deduction" in content)
        and "no withholding tax" not in content
        and "without withholding tax" not in content
    )
    service_matches = detect_all(content, SERVICE_RULES)
    return {
        "contract_path": str(path),
        "country": detect_first(content, COUNTRY_RULES),
        "currency": detect_first(content, CURRENCY_RULES),
        "service_type": service_matches[0] if service_matches else "Pendiente",
        "service_matches": service_matches,
        "payment_channel_hint": detect_first(content, PAYMENT_CHANNEL_RULES),
        "payment_terms": extract_payment_terms(content),
        "mentions_foreign_tax": mentions_foreign_tax,
        "mentions_acceptance": "acceptance" in content or "approved" in content,
        "mentions_reimbursements": "reimburs" in content or "expense" in content,
        "mentions_crypto": "crypto" in content or "usdt" in content or "bitcoin" in content,
    }


def write_markdown(data: dict, out_path: Path) -> None:
    lines = [
        "# Senales del contrato de exportacion",
        "",
        f"- Contrato: `{data['contract_path']}`",
        f"- Pais detectado: {data['country']}",
        f"- Moneda detectada: {data['currency']}",
        f"- Tipo de servicio detectado: {data['service_type']}",
        f"- Servicios detectados: {', '.join(data['service_matches']) if data['service_matches'] else 'ninguno'}",
        f"- Canal de cobro detectado: {data['payment_channel_hint']}",
        f"- Termino de pago detectado: {data['payment_terms']}",
        f"- Retencion extranjera visible: {'si' if data['mentions_foreign_tax'] else 'no'}",
        f"- Hito de aceptacion visible: {'si' if data['mentions_acceptance'] else 'no'}",
        f"- Reembolsos visibles: {'si' if data['mentions_reimbursements'] else 'no'}",
        f"- Cripto visible: {'si' if data['mentions_crypto'] else 'no'}",
    ]
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    data = parse_contract(Path(args.contract).resolve())
    (out_dir / "SenalesContratoExportacion.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    write_markdown(data, out_dir / "SenalesContratoExportacion.md")


if __name__ == "__main__":
    main()
