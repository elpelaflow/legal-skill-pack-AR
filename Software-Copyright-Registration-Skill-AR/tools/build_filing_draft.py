#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_draft(intake: dict, scan: dict) -> dict:
    return {
        "work_name": intake.get("work_name", "Pendiente"),
        "version": intake.get("version", "Pendiente"),
        "work_type": intake.get("work_type", "Pendiente"),
        "category": intake.get("category", "Pendiente"),
        "authors": intake.get("authors", []),
        "holder": intake.get("holder", "Pendiente"),
        "completion_date": intake.get("completion_date", "Pendiente"),
        "publication_date": intake.get("publication_date", "Pendiente"),
        "publication_place": intake.get("publication_place", "Pendiente"),
        "languages": list(scan.get("languages", {}).keys()),
        "estimated_lines": scan.get("estimated_lines", 0),
        "platform_notes": "Pendiente",
        "hardware_notes": "Pendiente",
    }


def write_markdown(path: Path, data: dict) -> None:
    lines = [
        "# Borrador de campos DNDA",
        "",
        f"- Nombre de la obra: {data['work_name']}",
        f"- Version: {data['version']}",
        f"- Tipo de obra: {data['work_type']}",
        f"- Categoria: {data['category']}",
        f"- Titular: {data['holder']}",
        f"- Fecha de finalizacion: {data['completion_date']}",
        f"- Fecha de publicacion: {data['publication_date']}",
        f"- Lugar de publicacion: {data['publication_place']}",
        f"- Lenguajes detectados: {', '.join(data['languages']) or 'Pendiente'}",
        f"- Lineas estimadas: {data['estimated_lines']}",
        "",
        "## Autores",
        "",
    ]
    for item in data["authors"] or ["Pendiente"]:
        lines.append(f"- {item}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intake", required=True)
    parser.add_argument("--scan", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    data = build_draft(load_json(Path(args.intake)), load_json(Path(args.scan)))
    (out_dir / "BorradorCamposDNDA.json").write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    write_markdown(out_dir / "BorradorCamposDNDA.md", data)


if __name__ == "__main__":
    main()
