#!/usr/bin/env python3
"""Preparar variantes de búsqueda previa y una planilla base de antecedentes marcarios."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


INPI_CONSULTA_URL = "https://portaltramites.inpi.gob.ar/MarcasConsultas/ConsultaTuMarca"
INPI_BUSQUEDA_URL = "https://portaltramites.inpi.gob.ar/MarcasConsultas/Busqueda"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def clean_spaces(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def normalize_word(word: str) -> str:
    return re.sub(r"[^A-Za-z0-9ÁÉÍÓÚáéíóúÑñÜü]", "", word).strip()


def split_camel_case(value: str) -> str:
    return re.sub(r"(?<=[a-záéíóúñ])(?=[A-ZÁÉÍÓÚÑ])", " ", value)


def build_variants(brand_name: str) -> list[str]:
    brand_name = clean_spaces(brand_name)
    if not brand_name:
        return []
    spaced_brand = clean_spaces(split_camel_case(brand_name))
    variants = {brand_name}
    variants.add(spaced_brand)
    lowered = brand_name.lower()
    lowered_spaced = spaced_brand.lower()
    variants.add(lowered)
    variants.add(lowered_spaced)
    compact = lowered.replace(" ", "")
    variants.add(compact)
    dashed = lowered.replace(" ", "-")
    variants.add(dashed)
    words = [normalize_word(part) for part in re.split(r"[\s\-_]+", spaced_brand) if normalize_word(part)]
    variants.update(words)
    if len(words) > 1:
        variants.add(" ".join(words[:2]))
        variants.add("-".join(words[:2]).lower())
    return sorted(item for item in variants if item)


def build_output(data: dict) -> dict:
    brand_name = str(data.get("brand_name") or "")
    variants = build_variants(brand_name)
    return {
        "brand_name": brand_name,
        "search_urls": {
            "consulta_tu_marca": INPI_CONSULTA_URL,
            "busqueda": INPI_BUSQUEDA_URL,
        },
        "search_variants": variants,
        "search_matrix": [
            {
                "query": query,
                "class_hint": "",
                "result_found": "",
                "matched_sign": "",
                "matched_class": "",
                "similarity_type": "",
                "risk_level": "",
                "status": "",
                "url": "",
                "notes": "",
            }
            for query in variants
        ],
        "summary": "",
        "risk_level": "",
        "confirmation_required": True,
        "user_confirmed": False,
    }


def write_markdown(path: Path, result: dict) -> None:
    lines = [
        "# Búsqueda de Antecedentes Marcarios",
        "",
        f"- Marca: {result.get('brand_name', '')}",
        f"- Consulta pública INPI: {INPI_CONSULTA_URL}",
        f"- Búsqueda pública INPI: {INPI_BUSQUEDA_URL}",
        "",
        "## Variantes sugeridas",
        "",
    ]
    lines.extend(f"- {item}" for item in result.get("search_variants", []))
    lines.extend(
        [
            "",
            "## Matriz de registro",
            "",
            "| Consulta | Clase | Resultado | Signo hallado | Tipo similitud | Riesgo | Estado | URL | Notas |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for item in result.get("search_matrix", []):
        lines.append(
            f"| {item['query']} |  |  |  |  |  |  |  |  |"
        )
    lines.extend(
        [
            "",
            "## Conclusión",
            "",
            "- Riesgo general: Pendiente",
            "- Recomendación: Pendiente",
            "",
            "```text",
            "STOP_FOR_USER",
            "NEXT_ACTION: Complete la búsqueda previa en la base pública del INPI y confirme si desea continuar con la marca.",
            "```",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--out-dir", default="MarcaINPI/Borradores")
    args = parser.parse_args()

    data = load_json(Path(args.input))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    result = build_output(data)
    (out_dir / "BusquedaAntecedentes.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_markdown(out_dir / "BusquedaAntecedentes.md", result)
    print(f"OK búsqueda preparada: {out_dir / 'BusquedaAntecedentes.md'}")
    print("STOP_FOR_USER")


if __name__ == "__main__":
    main()
