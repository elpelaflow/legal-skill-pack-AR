#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

GAINS_REDUCTION = {
    "micro": 0.60,
    "pequena": 0.60,
    "mediana": 0.40,
    "grande": 0.20,
}


def normalize_company_size(size: str) -> str:
    value = (size or "").strip().lower()
    mapping = {
        "micro": "micro",
        "pequena": "pequena",
        "pequeña": "pequena",
        "small": "pequena",
        "mediana": "mediana",
        "medium": "mediana",
        "grande": "grande",
        "large": "grande",
    }
    return mapping.get(value, "pendiente")


def build_estimate(data: dict) -> dict:
    size = normalize_company_size(data.get("company_size", ""))
    contributions = float(data.get("promoted_social_security_contributions", 0) or 0)
    gains_tax = float(data.get("promoted_gains_tax", 0) or 0)
    export_share = float(data.get("exports_share_numeric", 0) or 0)
    incentive_hires = int(data.get("incentive_hires", 0) or 0)

    base_credit = contributions * 0.70
    enhanced_credit = contributions * 0.80 if incentive_hires > 0 else 0
    gains_reduction_rate = GAINS_REDUCTION.get(size, 0)
    gains_reduction_amount = gains_tax * gains_reduction_rate
    transferability = "posible" if export_share >= 70 else "no_configurada"
    verification_fee_cap = (base_credit if enhanced_credit == 0 else enhanced_credit) * 0.04

    return {
        "company_size": size,
        "base_credit_fiscal": round(base_credit, 2),
        "enhanced_credit_fiscal_reference": round(enhanced_credit, 2),
        "gains_reduction_rate": gains_reduction_rate,
        "gains_reduction_amount": round(gains_reduction_amount, 2),
        "export_share_numeric": export_share,
        "bonus_transferability_reference": transferability,
        "verification_fee_cap_reference": round(verification_fee_cap, 2),
        "assumptions": [
            "La estimacion es orientativa y depende de inscripcion efectiva y parametrizacion fiscal.",
            "El bono estandar se calcula al 70% de contribuciones patronales promovidas.",
            "La referencia al 80% requiere verificar altas promocionadas alcanzadas por la ley.",
            "La reduccion de ganancias depende del tamano de empresa informado.",
        ],
    }


def write_markdown(data: dict, out_path: Path) -> None:
    lines = [
        "# Estimacion de beneficios LEC",
        "",
        f"- Tamano empresa: {data['company_size']}",
        f"- Bono credito fiscal 70%: {data['base_credit_fiscal']}",
        f"- Referencia bono 80%: {data['enhanced_credit_fiscal_reference']}",
        f"- Reduccion ganancias (%): {data['gains_reduction_rate'] * 100:.0f}",
        f"- Reduccion ganancias estimada: {data['gains_reduction_amount']}",
        f"- Exportaciones (%): {data['export_share_numeric']}",
        f"- Transferibilidad / uso en ganancias: {data['bonus_transferability_reference']}",
        f"- Tope referencial tasa verificacion (4%): {data['verification_fee_cap_reference']}",
        "",
        "## Supuestos",
        "",
    ]
    for assumption in data["assumptions"]:
        lines.append(f"- {assumption}")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    estimate = build_estimate(json.loads(Path(args.input).read_text(encoding="utf-8")))
    (out_dir / "EstimacionBeneficiosLEC.json").write_text(
        json.dumps(estimate, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    write_markdown(estimate, out_dir / "EstimacionBeneficiosLEC.md")


if __name__ == "__main__":
    main()
