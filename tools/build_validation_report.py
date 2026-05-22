#!/usr/bin/env python3
"""Consolidar reporte final de validación legal/documental."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", required=True)
    parser.add_argument("--reference-signals", required=True)
    parser.add_argument("--matrix", required=True)
    parser.add_argument("--out-dir", default="ValidacionLegalAR/Borradores")
    args = parser.parse_args()

    inventory = load_json(Path(args.inventory))
    reference_signals = load_json(Path(args.reference_signals))
    matrix = load_json(Path(args.matrix))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    critical_items = []
    for issue in reference_signals.get("issues", []):
        if matrix.get("overall_status") == "critico":
            critical_items.append(issue)

    lines = [
        "# Reporte de Validación Legal/Documental",
        "",
        f"- Estado general: {matrix.get('overall_status')}",
        f"- Archivos analizados: {inventory.get('summary', {}).get('files_total', 0)}",
        f"- Contexto esperado: {reference_signals.get('expected_context', 'general')}",
        "",
        "## Hallazgos críticos",
        "",
    ]
    if critical_items:
        lines.extend(f"- {item}" for item in critical_items)
    else:
        lines.append("- No se detectaron hallazgos críticos automáticos.")

    lines.extend([
        "",
        "## Observaciones por dimensión",
        "",
    ])
    for name, item in matrix.get("dimensions", {}).items():
        lines.append(f"### {name}")
        lines.append("")
        lines.append(f"- Estado: {item.get('status')}")
        for obs in item.get("observations", []):
            lines.append(f"- {obs}")
        lines.append("")

    lines.extend([
        "## Próximos pasos",
        "",
        "- Corregir referencias extranjeras impropias si aparecen sin justificación.",
        "- Unificar formato de fecha y moneda según el contexto argentino del documento.",
        "- Revisar manualmente cualquier PDF que no haya podido validarse.",
        "",
        "```text",
        "STOP_FOR_USER",
        "NEXT_ACTION: Revise el reporte y confirme qué observaciones desea corregir.",
        "```",
        "",
    ])

    (out_dir / "ReporteValidacionLegal.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"OK reporte: {out_dir / 'ReporteValidacionLegal.md'}")
    print("STOP_FOR_USER")


if __name__ == "__main__":
    main()
