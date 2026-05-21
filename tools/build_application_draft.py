#!/usr/bin/env python3
"""Consolidar un borrador de solicitud de marca para INPI Argentina."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def goods_by_class(data: dict) -> list[dict]:
    classes = data.get("classes", [])
    return [item for item in classes if isinstance(item, dict)]


def selected_classes(data: dict) -> list[int]:
    result: list[int] = []
    for item in data.get("candidates", []):
        if item.get("selected") is True:
            result.append(int(item["class_number"]))
    if result:
        return sorted(set(result))
    return sorted({int(item["class_number"]) for item in data.get("candidates", []) if item.get("score", 0) > 0})


def build(intake: dict, classes: dict, goods_services: dict, search: dict | None) -> dict:
    class_numbers = selected_classes(classes)
    return {
        "brand_name": intake.get("brand_name", ""),
        "brand_type": intake.get("brand_type", ""),
        "holder_name": intake.get("holder_name", ""),
        "holder_id": intake.get("holder_id", ""),
        "holder_country": intake.get("holder_country", "Argentina"),
        "holder_address": intake.get("holder_address", ""),
        "contact_email": intake.get("contact_email", ""),
        "has_logo": intake.get("has_logo", False),
        "claims_color": intake.get("claims_color", False),
        "foreign_priority": intake.get("foreign_priority", False),
        "priority_details": intake.get("priority_details", ""),
        "business_summary": intake.get("business_summary", ""),
        "selected_classes": class_numbers,
        "goods_services": goods_by_class(goods_services),
        "prior_search_summary": (search or {}).get("summary", ""),
        "prior_search_risk": (search or {}).get("risk_level", ""),
        "warnings": [],
        "confirmation_required": True,
        "user_confirmed": False,
    }


def add_warnings(draft: dict) -> None:
    if not draft.get("brand_name"):
        draft["warnings"].append("Falta la denominación exacta de la marca.")
    if not draft.get("holder_name"):
        draft["warnings"].append("Falta el titular.")
    if not draft.get("selected_classes"):
        draft["warnings"].append("No hay clases seleccionadas.")
    if not draft.get("goods_services"):
        draft["warnings"].append("No hay redacción de productos/servicios por clase.")
    if draft.get("foreign_priority") and not draft.get("priority_details"):
        draft["warnings"].append("Se indicó prioridad extranjera, pero faltan detalles.")


def write_markdown(path: Path, draft: dict) -> None:
    lines = [
        "# Solicitud de Marca (Borrador)",
        "",
        f"➤ **Marca**: {draft.get('brand_name') or 'Pendiente'}",
        f"➤ **Tipo de signo**: {draft.get('brand_type') or 'Pendiente'}",
        f"➤ **Titular**: {draft.get('holder_name') or 'Pendiente'}",
        f"➤ **CUIT/CUIL**: {draft.get('holder_id') or 'Pendiente'}",
        f"➤ **País del titular**: {draft.get('holder_country') or 'Pendiente'}",
        f"➤ **Domicilio**: {draft.get('holder_address') or 'Pendiente'}",
        f"➤ **Correo**: {draft.get('contact_email') or 'Pendiente'}",
        f"➤ **Logo**: {'Sí' if draft.get('has_logo') else 'No'}",
        f"➤ **Reivindica color**: {'Sí' if draft.get('claims_color') else 'No'}",
        f"➤ **Prioridad extranjera**: {'Sí' if draft.get('foreign_priority') else 'No'}",
        f"➤ **Detalle prioridad**: {draft.get('priority_details') or 'No informado'}",
        f"➤ **Clases seleccionadas**: {', '.join(str(item) for item in draft.get('selected_classes', [])) or 'Pendiente'}",
        "",
        "## Resumen del Negocio",
        "",
        draft.get("business_summary") or "Pendiente",
        "",
        "## Productos y Servicios por Clase",
        "",
    ]
    for item in draft.get("goods_services", []):
        lines.extend(
            [
                f"### Clase {item.get('class_number', 'Pendiente')}",
                "",
                item.get("description") or "Pendiente",
                "",
                f"- Motivo: {item.get('reason') or 'Pendiente'}",
                "",
            ]
        )
    lines.extend(
        [
            "## Búsqueda de Antecedentes",
            "",
            f"- Riesgo declarado: {draft.get('prior_search_risk') or 'No informado'}",
            f"- Resumen: {draft.get('prior_search_summary') or 'No informado'}",
            "",
            "## Advertencias",
            "",
        ]
    )
    warnings = draft.get("warnings", [])
    if warnings:
        lines.extend(f"- {warning}" for warning in warnings)
    else:
        lines.append("- Ninguna")
    lines.extend(
        [
            "",
            "```text",
            "STOP_FOR_USER",
            "NEXT_ACTION: Revise el borrador completo de la solicitud y confirme antes de presentar ante el INPI.",
            "```",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_class_markdown(path: Path, draft: dict, item: dict) -> None:
    class_number = item.get("class_number", "Pendiente")
    lines = [
        f"# Solicitud de Marca - Clase {class_number}",
        "",
        f"➤ **Marca**: {draft.get('brand_name') or 'Pendiente'}",
        f"➤ **Tipo de signo**: {draft.get('brand_type') or 'Pendiente'}",
        f"➤ **Titular**: {draft.get('holder_name') or 'Pendiente'}",
        f"➤ **CUIT/CUIL**: {draft.get('holder_id') or 'Pendiente'}",
        f"➤ **Domicilio**: {draft.get('holder_address') or 'Pendiente'}",
        f"➤ **Correo**: {draft.get('contact_email') or 'Pendiente'}",
        f"➤ **Clase**: {class_number}",
        f"➤ **Logo**: {'Sí' if draft.get('has_logo') else 'No'}",
        f"➤ **Reivindica color**: {'Sí' if draft.get('claims_color') else 'No'}",
        "",
        "## Productos o Servicios",
        "",
        item.get("description") or "Pendiente",
        "",
        f"- Motivo: {item.get('reason') or 'Pendiente'}",
        "",
        "## Búsqueda de Antecedentes",
        "",
        f"- Riesgo declarado: {draft.get('prior_search_risk') or 'No informado'}",
        f"- Resumen: {draft.get('prior_search_summary') or 'No informado'}",
        "",
        "## Advertencias",
        "",
    ]
    warnings = draft.get("warnings", [])
    if warnings:
        lines.extend(f"- {warning}" for warning in warnings)
    else:
        lines.append("- Ninguna")
    lines.extend(
        [
            "",
            "```text",
            "STOP_FOR_USER",
            "NEXT_ACTION: Revise este borrador de solicitud por clase antes de cargarlo en el portal del INPI.",
            "```",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intake", required=True)
    parser.add_argument("--classes", required=True)
    parser.add_argument("--goods-services", required=True)
    parser.add_argument("--search")
    parser.add_argument("--out-dir", default="MarcaINPI/Borradores")
    args = parser.parse_args()

    intake = load_json(Path(args.intake))
    classes = load_json(Path(args.classes))
    goods_services = load_json(Path(args.goods_services))
    search = load_json(Path(args.search)) if args.search else None

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    draft = build(intake, classes, goods_services, search)
    add_warnings(draft)

    (out_dir / "SolicitudMarca.json").write_text(
        json.dumps(draft, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_markdown(out_dir / "SolicitudMarca.md", draft)
    for item in draft.get("goods_services", []):
        class_number = item.get("class_number")
        if class_number in (None, ""):
            continue
        write_class_markdown(out_dir / f"SolicitudMarca_Clase{class_number}.md", draft, item)
    print(f"OK borrador de solicitud: {out_dir / 'SolicitudMarca.md'}")
    print("STOP_FOR_USER")


if __name__ == "__main__":
    main()
