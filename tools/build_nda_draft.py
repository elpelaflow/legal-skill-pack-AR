#!/usr/bin/env python3
"""Consolidar borrador de NDA para Argentina."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_md(path: Path, intake: dict, matrix: dict, signature: dict) -> None:
    lines = [
        "# Acuerdo de Confidencialidad (Borrador)",
        "",
        f"➤ **Parte A**: {intake.get('party_a') or 'Pendiente'}",
        f"➤ **Parte B**: {intake.get('party_b') or 'Pendiente'}",
        f"➤ **Tipo**: {matrix.get('nda_type') or 'Pendiente'}",
        f"➤ **Riesgo**: {matrix.get('risk_level') or 'Pendiente'}",
        "",
        "## 1. Propósito",
        "",
        matrix.get("purpose") or "Pendiente",
        "",
        "## 2. Información Confidencial",
        "",
        f"- {matrix.get('confidential_assets') or 'Pendiente'}",
        f"- Categorías: {matrix.get('asset_categories') or 'Pendiente'}",
        "",
        "## 3. Exclusiones",
        "",
    ]
    lines.extend(f"- {item}" for item in matrix.get("exclusions", []))
    lines.extend(
        [
            "",
            "## 3.1 Sharing permitido por necesidad de conocimiento",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in matrix.get("need_to_know_sharing", []))
    lines.extend(
        [
            "",
            "## 4. Plazo",
            "",
            f"- {matrix.get('term_summary') or 'Pendiente'}",
            "",
            "## 5. Firma",
            "",
            f"- Modalidad prevista: {signature.get('signature_mode') or 'Pendiente'}",
            f"- Observación: {signature.get('note') or 'Pendiente'}",
            f"- Cautela probatoria: {signature.get('evidence_level') or 'Pendiente'}",
            "",
            "## 6. Ley y jurisdicción",
            "",
            "- Pendiente completar.",
            "",
            "```text",
            "STOP_FOR_USER",
            "NEXT_ACTION: Revise el NDA y confirme antes de circularlo para firma.",
            "```",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intake", required=True)
    parser.add_argument("--matrix", required=True)
    parser.add_argument("--signature", required=True)
    parser.add_argument("--out-dir", default="AcuerdoConfidencialidad/Borradores")
    args = parser.parse_args()

    intake = load_json(Path(args.intake))
    matrix = load_json(Path(args.matrix))
    signature = load_json(Path(args.signature))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    write_md(out_dir / "AcuerdoConfidencialidad.md", intake, matrix, signature)
    print(f"OK nda: {out_dir / 'AcuerdoConfidencialidad.md'}")
    print("STOP_FOR_USER")


if __name__ == "__main__":
    main()
