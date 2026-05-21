#!/usr/bin/env python3
"""Consolidar especificación base de smart contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_md(path: Path, intake: dict, logic: dict, split: dict, risk: dict) -> None:
    lines = [
        "# Smart Contract Spec (Borrador)",
        "",
        f"➤ **Proyecto**: {intake.get('project_name') or 'Pendiente'}",
        f"➤ **Blockchain objetivo**: {intake.get('blockchain_target') or 'Pendiente'}",
        f"➤ **Acción automatizada**: {intake.get('automated_action') or 'Pendiente'}",
        f"➤ **Riesgo**: {risk.get('risk_level') or 'Pendiente'}",
        f"➤ **Patrón**: {risk.get('execution_pattern') or 'Pendiente'}",
        "",
        "## 1. Propósito de negocio",
        "",
        intake.get("business_purpose") or "Pendiente",
        "",
        "## 2. Lógica legal",
        "",
        f"- Acción: {logic.get('automated_action') or intake.get('automated_action') or 'Pendiente'}",
        "",
        "## 3. División on-chain / off-chain",
        "",
        f"- On-chain: {split.get('onchain') or 'Pendiente'}",
        f"- Off-chain: {split.get('offchain') or 'Pendiente'}",
        "",
        "## 4. Dependencias externas",
        "",
        f"- {split.get('external_dependencies') or 'Ninguna declarada'}",
        "",
        "## 5. Riesgos",
        "",
        f"- Flags: {risk.get('risk_flags') or 'Ninguno detectado automáticamente'}",
        "",
        "## 6. Controles requeridos",
        "",
        "- Pendiente completar: pausabilidad, roles, fallback, upgrade y evidencia.",
        "",
        "## 7. Patrón de ejecución sugerido",
        "",
        f"- {risk.get('execution_pattern') or 'Pendiente'}",
        "",
        "```text",
        "STOP_FOR_USER",
        "NEXT_ACTION: Revise la especificación y confirme antes de usarla como base legal o técnica.",
        "```",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intake", required=True)
    parser.add_argument("--logic", required=True)
    parser.add_argument("--split", required=True)
    parser.add_argument("--risk", required=True)
    parser.add_argument("--out-dir", default="SmartContractSpecAR/Borradores")
    args = parser.parse_args()

    intake = load_json(Path(args.intake))
    logic = load_json(Path(args.logic))
    split = load_json(Path(args.split))
    risk = load_json(Path(args.risk))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    write_md(out_dir / "SmartContractSpec.md", intake, logic, split, risk)
    print(f"OK spec: {out_dir / 'SmartContractSpec.md'}")
    print("STOP_FOR_USER")


if __name__ == "__main__":
    main()
