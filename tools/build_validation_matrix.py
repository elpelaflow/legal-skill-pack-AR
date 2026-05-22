#!/usr/bin/env python3
"""Construir matriz de validación documental."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def max_status(*items: str) -> str:
    order = {"ok": 0, "revisar": 1, "critico": 2}
    return max(items, key=lambda value: order[value])


def evaluate_language(files: list[dict]) -> tuple[str, list[str]]:
    observations: list[str] = []
    status = "ok"
    if any(item.get("english_months") for item in files if item["type"] == "text"):
        status = "revisar"
        observations.append("Se detectaron meses en inglés.")
    if any(item.get("foreign_signals") for item in files if item["type"] == "text"):
        status = max_status(status, "revisar")
        observations.append("Se detectaron señales de localización extranjera.")
    return status, observations


def evaluate_format(files: list[dict]) -> tuple[str, list[str]]:
    observations: list[str] = []
    status = "ok"
    if any(item.get("ambiguous_dates") for item in files if item["type"] == "text"):
        status = "revisar"
        observations.append("Se detectaron fechas numéricas ambiguas.")
    if any(item.get("usd_signals", 0) > 0 for item in files if item["type"] == "text"):
        status = max_status(status, "revisar")
        observations.append("Se detectaron referencias a moneda extranjera.")
    return status, observations


def evaluate_pdf(files: list[dict]) -> tuple[str, list[str]]:
    observations: list[str] = []
    pdfs = [item for item in files if item["type"] == "pdf"]
    if not pdfs:
        return "revisar", ["No se encontraron PDFs para validar formato final."]

    status = "ok"
    for item in pdfs:
        if item.get("analysis_status") != "ok":
            status = max_status(status, "revisar")
            observations.append(f"El PDF {item['path']} no pudo validarse automáticamente.")
            continue
        if item.get("all_a4") is False:
            status = max_status(status, "critico")
            observations.append(f"El PDF {item['path']} no está completamente en A4.")
    if not observations:
        observations.append("Los PDFs analizados parecen estar en A4.")
    return status, observations


def write_markdown(path: Path, matrix: dict) -> None:
    lines = [
        "# Matriz de Validación",
        "",
        f"- Estado general: {matrix['overall_status']}",
        "",
        "## Dimensiones",
        "",
    ]
    for name, item in matrix["dimensions"].items():
        lines.append(f"- {name}: {item['status']}")
        for obs in item["observations"]:
            lines.append(f"  - {obs}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", required=True)
    parser.add_argument("--reference-signals", required=True)
    parser.add_argument("--out-dir", default="ValidacionLegalAR/Borradores")
    args = parser.parse_args()

    inventory = load_json(Path(args.inventory))
    reference_signals = load_json(Path(args.reference_signals))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    files = inventory.get("files", [])
    language_status, language_obs = evaluate_language(files)
    format_status, format_obs = evaluate_format(files)
    pdf_status, pdf_obs = evaluate_pdf(files)
    references_status = reference_signals.get("status", "revisar")

    matrix = {
        "overall_status": max_status(language_status, format_status, pdf_status, references_status),
        "dimensions": {
            "lenguaje_localizacion": {
                "status": language_status,
                "observations": language_obs,
            },
            "referencias_contexto": {
                "status": references_status,
                "observations": reference_signals.get("issues", []),
            },
            "formato": {
                "status": format_status,
                "observations": format_obs,
            },
            "pdf_final": {
                "status": pdf_status,
                "observations": pdf_obs,
            },
        },
    }
    (out_dir / "MatrizValidacion.json").write_text(
        json.dumps(matrix, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    write_markdown(out_dir / "MatrizValidacion.md", matrix)
    print(f"OK matriz: {out_dir / 'MatrizValidacion.json'}")


if __name__ == "__main__":
    main()
