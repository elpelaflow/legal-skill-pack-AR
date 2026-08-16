#!/usr/bin/env python3
"""Inventariar documentos y detectar señales base de validación."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

try:
    from pypdf import PdfReader  # type: ignore
except Exception:  # pragma: no cover - dependencia opcional
    PdfReader = None


TEXT_EXTENSIONS = {".md", ".txt", ".json"}
FOREIGN_SIGNALS = [
    "rgpd",
    "gdpr",
    "cnipa",
    "delaware law",
    "nif",
    "cif",
    "vosotros",
]
ARGENTINA_SIGNALS = [
    "aaip",
    "inpi",
    "dnda",
    "arca",
    "bcra",
    "tad",
    "ley 25.326",
    "ley 25.506",
    "ley 11.723",
    "ley 24.481",
    "ley 27.506",
]
MONTHS_EN = [
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
]
DATE_SLASH_RE = re.compile(r"\b\d{1,2}/\d{1,2}/\d{4}\b")
CUIT_RE = re.compile(r"\b\d{2}-\d{8}-\d\b")
ARS_RE = re.compile(r"\bARS\b|\$\s?\d")
USD_RE = re.compile(r"\bUSD\b|\bUS\$\b")


def read_text_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")


def count_signals(text: str, items: list[str]) -> dict[str, int]:
    lowered = text.lower()
    return {item: lowered.count(item) for item in items if item in lowered}


def analyze_text_file(base_dir: Path, path: Path) -> dict:
    text = read_text_file(path)
    lowered = text.lower()
    return {
        "path": str(path.relative_to(base_dir)),
        "type": "text",
        "extension": path.suffix.lower(),
        "characters": len(text),
        "foreign_signals": count_signals(text, FOREIGN_SIGNALS),
        "argentina_signals": count_signals(text, ARGENTINA_SIGNALS),
        "ambiguous_dates": DATE_SLASH_RE.findall(text),
        "english_months": [month for month in MONTHS_EN if month in lowered],
        "cuit_matches": CUIT_RE.findall(text),
        "ars_signals": len(ARS_RE.findall(text)),
        "usd_signals": len(USD_RE.findall(text)),
    }


def points_to_mm(value: float) -> float:
    return value * 25.4 / 72.0


def is_a4(width_mm: float, height_mm: float) -> bool:
    pair = sorted([width_mm, height_mm])
    target = [210.0, 297.0]
    return all(abs(pair[index] - target[index]) <= 2.0 for index in range(2))


def analyze_pdf_file(base_dir: Path, path: Path) -> dict:
    pdf_info = {
        "path": str(path.relative_to(base_dir)),
        "type": "pdf",
        "extension": ".pdf",
        "pages": None,
        "page_sizes_mm": [],
        "all_a4": None,
        "analysis_status": "pending",
    }
    if PdfReader is None:
        pdf_info["analysis_status"] = "pypdf_not_installed"
        return pdf_info

    try:
        reader = PdfReader(str(path))
        sizes = []
        all_a4 = True
        for page in reader.pages:
            box = page.mediabox
            width = points_to_mm(float(box.width))
            height = points_to_mm(float(box.height))
            sizes.append({
                "width_mm": round(width, 1),
                "height_mm": round(height, 1),
                "is_a4": is_a4(width, height),
            })
            all_a4 = all_a4 and sizes[-1]["is_a4"]
        pdf_info["pages"] = len(reader.pages)
        pdf_info["page_sizes_mm"] = sizes
        pdf_info["all_a4"] = all_a4
        pdf_info["analysis_status"] = "ok"
    except Exception as exc:  # pragma: no cover - manejo defensivo
        pdf_info["analysis_status"] = f"error:{exc.__class__.__name__}"
    return pdf_info


def write_markdown(path: Path, files: list[dict], summary: dict) -> None:
    lines = [
        "# Inventario Documental",
        "",
        f"- Archivos analizados: {summary['files_total']}",
        f"- Archivos de texto: {summary['text_files']}",
        f"- PDFs: {summary['pdf_files']}",
        f"- Señales extranjeras detectadas: {summary['foreign_signals_total']}",
        f"- Señales argentinas detectadas: {summary['argentina_signals_total']}",
        "",
        "## Archivos",
        "",
    ]
    for item in files:
        lines.append(f"- {item['path']} ({item['type']})")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--out-dir", default="ValidacionLegalAR/Borradores")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    files: list[dict] = []
    for path in sorted(input_dir.rglob("*")):
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        if suffix in TEXT_EXTENSIONS:
            files.append(analyze_text_file(input_dir, path))
        elif suffix == ".pdf":
            files.append(analyze_pdf_file(input_dir, path))

    summary = {
        "files_total": len(files),
        "text_files": sum(1 for item in files if item["type"] == "text"),
        "pdf_files": sum(1 for item in files if item["type"] == "pdf"),
        "foreign_signals_total": sum(sum(item.get("foreign_signals", {}).values()) for item in files),
        "argentina_signals_total": sum(sum(item.get("argentina_signals", {}).values()) for item in files),
    }
    payload = {
        "input_dir": str(input_dir),
        "files": files,
        "summary": summary,
    }
    (out_dir / "InventarioDocumental.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    write_markdown(out_dir / "InventarioDocumental.md", files, summary)
    print(f"OK inventario: {out_dir / 'InventarioDocumental.json'}")


if __name__ == "__main__":
    main()
