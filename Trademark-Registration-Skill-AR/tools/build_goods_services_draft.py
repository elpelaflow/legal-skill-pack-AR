#!/usr/bin/env python3
"""Generar un primer borrador de productos y servicios a partir de clases sugeridas."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


CLASS_TEMPLATES = {
    9: {
        "description": "Aplicaciones de software descargables para {focus}.",
        "reason": "La oferta incluye software o apps descargables.",
    },
    35: {
        "description": "Servicios de marketplace, comercialización y administración comercial en línea relacionados con {focus}.",
        "reason": "La oferta incluye intermediación comercial, retail digital o promoción comercial.",
    },
    36: {
        "description": "Servicios financieros digitales relacionados con {focus}.",
        "reason": "La actividad incluye pagos, finanzas o herramientas financieras prestadas al público.",
    },
    41: {
        "description": "Servicios de educación, capacitación y contenidos en línea relacionados con {focus}.",
        "reason": "La actividad incluye enseñanza, formación o contenidos educativos.",
    },
    42: {
        "description": "Software como servicio (SaaS) y servicios tecnológicos en línea para {focus}.",
        "reason": "La oferta principal consiste en software o infraestructura tecnológica prestada en línea.",
    },
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def selected_classes(data: dict) -> list[int]:
    result = []
    for item in data.get("candidates", []):
        if item.get("selected") is True:
            result.append(int(item["class_number"]))
    if result:
        return sorted(set(result))
    return sorted({int(item["class_number"]) for item in data.get("candidates", [])})


def fallback_description(class_number: int, focus: str) -> dict:
    return {
        "class_number": class_number,
        "description": f"Productos o servicios de la clase {class_number} relacionados con {focus}.",
        "reason": "Se requiere ajuste manual específico para esta clase.",
    }


def build(intake: dict, classes: dict) -> dict:
    focus = (
        intake.get("business_summary")
        or ", ".join(str(item) for item in intake.get("current_offering", []))
        or "la actividad del titular"
    )
    items = []
    for class_number in selected_classes(classes):
        template = CLASS_TEMPLATES.get(class_number)
        if not template:
            items.append(fallback_description(class_number, focus))
            continue
        items.append(
            {
                "class_number": class_number,
                "description": template["description"].format(focus=focus),
                "reason": template["reason"],
            }
        )
    return {"classes": items, "confirmation_required": True, "user_confirmed": False}


def write_markdown(path: Path, result: dict) -> None:
    lines = ["# Productos y Servicios", ""]
    for item in result.get("classes", []):
        lines.extend(
            [
                f"## Clase {item['class_number']}",
                "",
                item["description"],
                "",
                f"- Motivo: {item['reason']}",
                "",
            ]
        )
    lines.extend(
        [
            "```text",
            "STOP_FOR_USER",
            "NEXT_ACTION: Ajuste y confirme la redacción final de productos y servicios por clase.",
            "```",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intake", required=True)
    parser.add_argument("--classes", required=True)
    parser.add_argument("--out-dir", default="MarcaINPI/Borradores")
    args = parser.parse_args()

    intake = load_json(Path(args.intake))
    classes = load_json(Path(args.classes))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    result = build(intake, classes)
    (out_dir / "ProductosServicios.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_markdown(out_dir / "ProductosServicios.md", result)
    print(f"OK productos/servicios: {out_dir / 'ProductosServicios.md'}")
    print("STOP_FOR_USER")


if __name__ == "__main__":
    main()
